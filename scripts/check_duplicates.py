#!/usr/bin/env python3
"""
Check and Clean Duplicate Notifications
This script helps identify and fix duplicate notification issues
"""

import os
import sys
import django

# Add the parent directory to Python path to find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webNotificationDjango.settings')
django.setup()

from django.utils import timezone
from home.models import ScheduledNotification

def check_notifications():
    """Check all notifications and identify issues"""
    print("🔍 Checking notification status...")
    print("=" * 60)
    
    # Get all notifications
    all_notifications = ScheduledNotification.objects.all().order_by('-created_at')
    
    print(f"📊 Total notifications: {all_notifications.count()}")
    
    # Count by status
    pending = ScheduledNotification.objects.filter(status='pending').count()
    sent = ScheduledNotification.objects.filter(status='sent').count()
    failed = ScheduledNotification.objects.filter(status='failed').count()
    
    print(f"⏳ Pending: {pending}")
    print(f"✅ Sent: {sent}")
    print(f"❌ Failed: {failed}")
    print()
    
    # Check for duplicates (same title, body, and scheduled time)
    print("🔍 Checking for potential duplicates...")
    duplicates = []
    
    for notification in all_notifications:
        similar = ScheduledNotification.objects.filter(
            title=notification.title,
            body=notification.body,
            scheduled_at=notification.scheduled_at,
            fcm_token=notification.fcm_token
        )
        
        if similar.count() > 1:
            duplicates.append({
                'title': notification.title,
                'count': similar.count(),
                'notifications': list(similar.values_list('id', 'status', 'created_at'))
            })
    
    if duplicates:
        print(f"⚠️  Found {len(duplicates)} potential duplicate groups:")
        for dup in duplicates:
            print(f"   📝 '{dup['title']}' - {dup['count']} instances")
            for notif_id, status, created in dup['notifications']:
                print(f"      ID: {notif_id}, Status: {status}, Created: {created}")
        print()
    else:
        print("✅ No obvious duplicates found")
    
    # Check for stuck notifications
    now = timezone.now()
    stuck = ScheduledNotification.objects.filter(
        status='pending',
        scheduled_at__lt=now - timezone.timedelta(minutes=5)  # More than 5 minutes old
    )
    
    if stuck.exists():
        print(f"⚠️  Found {stuck.count()} stuck notifications (scheduled more than 5 minutes ago):")
        for notification in stuck:
            print(f"   📝 '{notification.title}' - Scheduled: {notification.scheduled_at}")
        print()
    else:
        print("✅ No stuck notifications found")
    
    return duplicates, stuck

def clean_duplicates():
    """Clean up duplicate notifications"""
    print("🧹 Cleaning up duplicates...")
    
    # Find duplicates and keep only the first one
    duplicates_found = 0
    
    for notification in ScheduledNotification.objects.all():
        similar = ScheduledNotification.objects.filter(
            title=notification.title,
            body=notification.body,
            scheduled_at=notification.scheduled_at,
            fcm_token=notification.fcm_token
        ).order_by('created_at')
        
        if similar.count() > 1:
            # Keep the first one, delete the rest
            to_delete = similar[1:]  # All except the first
            for dup in to_delete:
                print(f"🗑️  Deleting duplicate: ID {dup.id} - '{dup.title}'")
                dup.delete()
                duplicates_found += 1
    
    if duplicates_found > 0:
        print(f"✅ Cleaned up {duplicates_found} duplicate notifications")
    else:
        print("✅ No duplicates to clean")

def reset_stuck_notifications():
    """Reset stuck notifications to pending"""
    now = timezone.now()
    stuck = ScheduledNotification.objects.filter(
        status='pending',
        scheduled_at__lt=now - timezone.timedelta(minutes=5)
    )
    
    if stuck.exists():
        print(f"🔄 Resetting {stuck.count()} stuck notifications...")
        for notification in stuck:
            print(f"   🔄 Resetting: '{notification.title}'")
            notification.status = 'pending'
            notification.save()
        print("✅ Stuck notifications reset")
    else:
        print("✅ No stuck notifications to reset")

def main():
    """Main function"""
    print("🔍 NOTIFICATION DUPLICATE CHECKER")
    print("=" * 60)
    
    # Check current status
    duplicates, stuck = check_notifications()
    
    print("\n🛠️  Available actions:")
    print("1. Clean duplicates")
    print("2. Reset stuck notifications")
    print("3. Both")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        clean_duplicates()
    elif choice == '2':
        reset_stuck_notifications()
    elif choice == '3':
        clean_duplicates()
        reset_stuck_notifications()
    elif choice == '4':
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice")
        return
    
    print("\n" + "=" * 60)
    print("🔍 Final status after cleanup:")
    check_notifications()

if __name__ == "__main__":
    main()
