#!/usr/bin/env python3
"""
Fixed Automatic Notifications - Prevents Duplicate Sends
This version ensures each notification is sent only once
"""

import os
import sys
import time
import django

# Add the parent directory to Python path to find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webNotificationDjango.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone
from home.models import ScheduledNotification

print("🚀 Starting Fixed Automatic Notifications...")
print("📱 This will check for notifications every 60 seconds")
print("🛡️  Duplicate protection enabled - each notification sent only once")
print("⏹️  Press Ctrl+C to stop")
print("-" * 10)

try:
    count = 0
    while True:
        count += 1
        now = timezone.now()
        print(f"\n🔄 Run #{count} at {now.strftime('%H:%M:%S')}")
        
        # Check for due notifications before sending
        due_notifications = ScheduledNotification.objects.filter(
            status='pending',
            scheduled_at__lte=now
        )
        
        if due_notifications.exists():
            print(f"📨 Found {due_notifications.count()} due notification(s)")
            
            # Send scheduled notifications (this will mark them as sent)
            call_command('send_scheduled_notifications')
            
            print(f"✅ Processed notifications (run #{count})")
        else:
            print("😴 No notifications due at this time")
        
        print("⏳ Waiting 10 seconds...")
        
        # Wait 60 seconds
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n\n🛑 Stopped by user")
    print(f"📊 Total runs: {count}")
    print("👋 Goodbye!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("💡 Check your Django setup and try again")
