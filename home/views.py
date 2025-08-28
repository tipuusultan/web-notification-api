from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
import json
from datetime import datetime, timedelta
from .models import UserFCMToken, ScheduledNotification
from .notification_service import fcm_service

def index(request):
    """Main page with notification permission interface"""
    return render(request, 'home/index.html')

def test_page(request):
    """Service worker test page"""
    return render(request, 'home/test.html')

def simple_test(request):
    """Simple service worker test page"""
    return render(request, 'home/simple_test.html')

def firebase_test(request):
    """Firebase configuration test page"""
    return render(request, 'home/firebase_test.html')

def service_worker(request):
    """Serve the Firebase messaging service worker"""
    response = HttpResponse(
        open('home/templates/firebase-messaging-sw.js', 'r').read(),
        content_type='application/javascript'
    )
    response['Service-Worker-Allowed'] = '/'
    return response

@csrf_exempt
@require_http_methods(["POST"])
def save_fcm_token(request):
    """API endpoint to save user FCM token"""
    try:
        data = json.loads(request.body)
        token = data.get('token')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        if not token:
            return JsonResponse({
                'success': False,
                'error': 'FCM token is required'
            }, status=400)
        
        # Check if token already exists
        fcm_token_obj, created = UserFCMToken.objects.get_or_create(
            token=token,
            defaults={
                'user_agent': user_agent,
                'is_active': True
            }
        )
        
        if not created:
            # Update existing token
            fcm_token_obj.user_agent = user_agent
            fcm_token_obj.is_active = True
            fcm_token_obj.save()
        
        return JsonResponse({
            'success': True,
            'message': 'FCM token saved successfully',
            'created': created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def schedule_notification(request):
    """API endpoint to schedule a notification"""
    try:
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('body')
        fcm_token = data.get('fcm_token')
        scheduled_at = data.get('scheduled_at')
        priority = data.get('priority', 'normal')
        
        if not all([title, body, fcm_token, scheduled_at]):
            return JsonResponse({
                'success': False,
                'error': 'Title, body, FCM token, and scheduled_at are required'
            }, status=400)
        
        try:
            # Parse scheduled_at (expecting ISO format)
            scheduled_datetime = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid scheduled_at format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            }, status=400)
        
        # Check if FCM token exists
        try:
            fcm_token_obj = UserFCMToken.objects.get(token=fcm_token, is_active=True)
        except UserFCMToken.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid or inactive FCM token'
            }, status=400)
        
        # Create scheduled notification
        notification = ScheduledNotification.objects.create(
            title=title,
            body=body,
            fcm_token=fcm_token_obj,
            scheduled_at=scheduled_datetime,
            priority=priority
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Notification scheduled successfully',
            'notification_id': notification.id,
            'scheduled_at': notification.scheduled_at.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def check_and_send_notifications(request):
    """API endpoint to check and send scheduled notifications"""
    try:
        now = timezone.now()
        
        # Get pending notifications that are due
        pending_notifications = ScheduledNotification.objects.filter(
            status='pending',
            scheduled_at__lte=now
        ).select_related('fcm_token')
        
        if not pending_notifications.exists():
            return JsonResponse({
                'success': True,
                'message': 'No pending notifications to send',
                'count': 0
            })
        
        sent_count = 0
        failed_count = 0
        
        for notification in pending_notifications:
            try:
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
                else:
                    notification.status = 'failed'
                    notification.error_message = result.get('error', 'Unknown error')
                    notification.save()
                    failed_count += 1
                    
            except Exception as e:
                notification.status = 'failed'
                notification.error_message = str(e)
                notification.save()
                failed_count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'Processed {len(pending_notifications)} notifications',
            'sent': sent_count,
            'failed': failed_count,
            'total': len(pending_notifications)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_notification_status(request):
    """API endpoint to get notification statistics"""
    try:
        total_tokens = UserFCMToken.objects.filter(is_active=True).count()
        total_scheduled = ScheduledNotification.objects.count()
        pending_notifications = ScheduledNotification.objects.filter(status='pending').count()
        sent_notifications = ScheduledNotification.objects.filter(status='sent').count()
        failed_notifications = ScheduledNotification.objects.filter(status='failed').count()
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_tokens': total_tokens,
                'total_scheduled': total_scheduled,
                'pending': pending_notifications,
                'sent': sent_notifications,
                'failed': failed_notifications
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_timezone_info(request):
    """API endpoint to get timezone information"""
    try:
        from .utils import get_timezone_info
        
        info = get_timezone_info()
        
        return JsonResponse({
            'success': True,
            'data': {
                'server_time': info['local_time'],
                'utc_time': info['utc_time'],
                'timezone': info['timezone'],
                'offset_hours': info['offset_hours'],
                'is_dst': info['is_dst']
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def send_notification(request):
    """Legacy endpoint - redirects to new system"""
    return JsonResponse({
        'success': False,
        'message': 'Use /api/schedule-notification/ to schedule notifications'
    })