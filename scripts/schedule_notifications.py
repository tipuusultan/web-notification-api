#!/usr/bin/env python3
"""
Interactive Notification Scheduler
Schedule various types of notifications using the API endpoints
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta

# Add the parent directory to Python path to find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webNotificationDjango.settings')
import django
django.setup()

from home.utils import schedule_for_minutes_from_now, schedule_for_local_time, get_timezone_info
from home.models import ScheduledNotification, UserFCMToken

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FCM_TOKEN = None  # Will be set when you run the script

def get_fcm_token():
    """Get FCM token from user input or database"""
    global FCM_TOKEN
    
    if FCM_TOKEN:
        return FCM_TOKEN
    
    print("🔑 FCM Token Required!")
    print("1. Visit http://127.0.0.1:8000/")
    print("2. Enable notifications and copy your FCM token")
    print("3. Paste it here:")
    
    FCM_TOKEN = input("FCM Token: ").strip()
    
    if not FCM_TOKEN:
        print("❌ No FCM token provided. Exiting.")
        sys.exit(1)
    
    return FCM_TOKEN

def schedule_notification(title, body, scheduled_at, priority="normal"):
    """Schedule a notification via API"""
    
    fcm_token = get_fcm_token()
    
    notification_data = {
        "title": title,
        "body": body,
        "fcm_token": fcm_token,
        "scheduled_at": scheduled_at,
        "priority": priority
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/schedule-notification/",
            json=notification_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scheduled: {title}")
            print(f"   Time: {scheduled_at}")
            print(f"   ID: {result['notification_id']}")
            return result['notification_id']
        else:
            print(f"❌ Failed to schedule: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error scheduling notification: {str(e)}")
        return None

def show_timezone_info():
    """Display current timezone information"""
    info = get_timezone_info()
    print("\n🌍 Timezone Information:")
    print(f"   Local Time: {info['local_time']}")
    print(f"   UTC Time: {info['utc_time']}")
    print(f"   Timezone: {info['timezone']}")
    print(f"   Offset: UTC{info['offset_hours']:+d}:30")
    print(f"   DST: {'Yes' if info['is_dst'] else 'No'}")

def schedule_test_notifications():
    """Schedule some test notifications"""
    print("\n🧪 Scheduling Test Notifications...")
    
    # Test 1: 2 minutes from now
    scheduled_time = schedule_for_minutes_from_now(2)
    schedule_notification(
        "🧪 Test Notification 1",
        "This notification was scheduled 2 minutes from now!",
        scheduled_time,
        "high"
    )
    
    # Test 2: 5 minutes from now
    scheduled_time = schedule_for_minutes_from_now(5)
    schedule_notification(
        "🧪 Test Notification 2", 
        "This notification was scheduled 5 minutes from now!",
        scheduled_time,
        "normal"
    )
    
    # Test 3: Tomorrow at 9 AM
    scheduled_time = schedule_for_local_time(9, 0, 1)
    schedule_notification(
        "🌅 Tomorrow's Reminder",
        "Good morning! Don't forget to check your tasks.",
        scheduled_time,
        "normal"
    )

def schedule_daily_reminders():
    """Schedule daily reminder notifications"""
    print("\n📅 Scheduling Daily Reminders...")
    
    # Daily reminder at 9 AM
    scheduled_time = schedule_for_local_time(9, 0, 0) # Changed to schedule_for_local_time
    schedule_notification(
        "🌅 Daily Morning Reminder",
        "Good morning! Time to start your day.",
        scheduled_time,
        "normal"
    )
    
    # Daily reminder at 6 PM
    scheduled_time = schedule_for_local_time(18, 0, 0) # Changed to schedule_for_local_time
    schedule_notification(
        "🌆 Daily Evening Reminder",
        "Evening reminder: Review your day's progress.",
        scheduled_time,
        "normal"
    )

def schedule_weekly_reminders():
    """Schedule weekly reminder notifications"""
    print("\n📆 Scheduling Weekly Reminders...")
    
    # Monday at 10 AM (weekday 0 = Monday)
    scheduled_time = schedule_for_local_time(10, 0, 0) # Changed to schedule_for_local_time
    schedule_notification(
        "📊 Weekly Planning",
        "Monday morning: Plan your week ahead!",
        scheduled_time,
        "high"
    )
    
    # Friday at 5 PM (weekday 4 = Friday)
    scheduled_time = schedule_for_local_time(17, 0, 0) # Changed to schedule_for_local_time
    schedule_notification(
        "🎉 Weekend Planning",
        "Friday evening: Plan your weekend activities!",
        scheduled_time,
        "normal"
    )

def schedule_custom_notification():
    """Schedule a custom notification"""
    print("\n✏️ Schedule Custom Notification...")
    
    # Get user input
    title = input("Notification title: ").strip()
    if not title:
        print("❌ Title is required")
        return
    
    body = input("Notification message: ").strip()
    if not body:
        print("❌ Message is required")
        return
    
    # Get scheduling options
    print("\nWhen would you like to send this notification?")
    print("1. In X minutes")
    print("2. In X hours")
    print("3. At specific time today")
    print("4. At specific time tomorrow")
    print("5. Custom date/time")
    
    choice = input("Choose option (1-5): ").strip()
    
    if choice == "1":
        minutes = int(input("Minutes from now: "))
        scheduled_time = schedule_for_minutes_from_now(minutes)
    elif choice == "2":
        hours = int(input("Hours from now: "))
        scheduled_time = schedule_for_minutes_from_now(hours * 60) # Changed to schedule_for_minutes_from_now
    elif choice == "3":
        time_str = input("Time today (HH:MM, e.g., 14:30): ")
        hour, minute = map(int, time_str.split(':'))
        scheduled_time = schedule_for_local_time(hour, minute, 0)
    elif choice == "4":
        time_str = input("Time tomorrow (HH:MM, e.g., 09:00): ")
        hour, minute = map(int, time_str.split(':'))
        scheduled_time = schedule_for_local_time(hour, minute, 1)
    elif choice == "5":
        date_str = input("Date (YYYY-MM-DD): ")
        time_str = input("Time (HH:MM): ")
        hour, minute = map(int, time_str.split(':'))
        year, month, day = map(int, date_str.split('-'))
        scheduled_time = schedule_for_local_time(hour, minute, 0)
        # Override the date calculation
        from datetime import date
        target_date = date(year, month, day)
        from django.utils import timezone
        from datetime import datetime, time
        scheduled_time = datetime.combine(target_date, time(hour, minute))
        scheduled_time = timezone.make_aware(scheduled_time)
        scheduled_time = scheduled_time.isoformat()
    else:
        print("❌ Invalid choice")
        return
    
    # Get priority
    priority = input("Priority (low/normal/high) [default: normal]: ").strip().lower()
    if priority not in ['low', 'normal', 'high']:
        priority = 'normal'
    
    # Schedule the notification
    schedule_notification(title, body, scheduled_time, priority)

def main():
    """Main menu"""
    print("🔔 Notification Scheduler")
    print("=" * 40)
    
    show_timezone_info()
    
    while True:
        print("\n📋 Menu:")
        print("1. Schedule test notifications")
        print("2. Schedule daily reminders")
        print("3. Schedule weekly reminders")
        print("4. Schedule custom notification")
        print("5. Show timezone info")
        print("6. Exit")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == "1":
            schedule_test_notifications()
        elif choice == "2":
            schedule_daily_reminders()
        elif choice == "3":
            schedule_weekly_reminders()
        elif choice == "4":
            schedule_custom_notification()
        elif choice == "5":
            show_timezone_info()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
