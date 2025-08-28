from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import ScheduledNotification
from home.notification_service import fcm_service
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send scheduled notifications that are due'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Maximum number of notifications to process (default: 100)',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        
        now = timezone.now()
        
        # Get pending notifications that are due
        pending_notifications = ScheduledNotification.objects.filter(
            status='pending',
            scheduled_at__lte=now
        ).select_related('fcm_token')[:limit]
        
        if not pending_notifications.exists():
            self.stdout.write(
                self.style.SUCCESS('No pending notifications to send')
            )
            return
        
        self.stdout.write(
            f'Found {len(pending_notifications)} pending notifications to send'
        )
        
        sent_count = 0
        failed_count = 0
        
        for notification in pending_notifications:
            try:
                if dry_run:
                    self.stdout.write(
                        f'[DRY RUN] Would send: "{notification.title}" to {notification.fcm_token.token[:30]}...'
                    )
                    sent_count += 1
                    continue
                
                # Send notification
                result = fcm_service.send_notification(
                    notification.fcm_token.token,
                    notification.title,
                    notification.body,
                    notification.priority
                )
                
                if result['success']:
                    notification.status = 'sent'
                    notification.sent_at = result.get('sent_at', timezone.now())
                    notification.save()
                    sent_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Sent: "{notification.title}" (ID: {notification.id})'
                        )
                    )
                else:
                    notification.status = 'failed'
                    notification.error_message = result.get('error', 'Unknown error')
                    notification.save()
                    failed_count += 1
                    
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Failed: "{notification.title}" (ID: {notification.id}) - {result.get("error")}'
                        )
                    )
                    
            except Exception as e:
                notification.status = 'failed'
                notification.error_message = str(e)
                notification.save()
                failed_count += 1
                
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error: "{notification.title}" (ID: {notification.id}) - {str(e)}'
                    )
                )
        
        # Summary
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\n[DRY RUN] Would have sent {sent_count} notifications'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Successfully sent {sent_count} notifications'
                )
            )
            
            if failed_count > 0:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Failed to send {failed_count} notifications'
                    )
                )
            
            self.stdout.write(
                f'📊 Total processed: {sent_count + failed_count}'
            )
