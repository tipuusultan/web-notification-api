#!/usr/bin/env python3
"""
Simple test script to schedule a notification
"""

import os
import sys
import django

# Add the parent directory to Python path to find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webNotificationDjango.settings')
django.setup()

from home.utils import schedule_for_minutes_from_now
from home.models import ScheduledNotification, UserFCMToken

def test_schedule():
    """Test scheduling a notification"""
    
    # Get first available FCM token
    token = UserFCMToken.objects.first()
    
    if not token:
        print("❌ No FCM tokens found. Please visit the web interface first.")
        return
    
    print(f"✅ Found FCM token: {token.token[:30]}...")
    
    # Schedule notification for 2 minutes from now
    scheduled_time = schedule_for_minutes_from_now(2)
    
    # Create the notification
    notification = ScheduledNotification.objects.create(
        title='🧪 New Test Notification',
        body='This notification was scheduled via test script!',
        fcm_token=token,
        scheduled_at=scheduled_time,
        priority='high'
    )
    
    print(f"✅ Notification scheduled successfully!")
    print(f"   ID: {notification.id}")
    print(f"   Title: {notification.title}")
    print(f"   Scheduled for: {scheduled_time}")
    print(f"   Status: {notification.status}")
    
    print(f"\n📋 To send this notification, run:")
    print(f"   python3 manage.py send_scheduled_notifications")

if __name__ == "__main__":
    test_schedule()
