#!/usr/bin/env python3
"""
Test script for the Django notification system
This script demonstrates how to use the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the Django server
BASE_URL = "http://localhost:8000"

def test_save_fcm_token():
    """Test saving an FCM token"""
    print("🔑 Testing FCM token save...")
    
    # Sample FCM token (replace with a real one for testing)
    token_data = {
        "token": "fKvO_57zggOCIlOuGk1ZnR:APA91bHwaBY35uuX70NgTk4B2WY9VC1hAM9KLId5PeV5zP2TJi2r4I6s7BlVeU9McxWeCBWoLjyd0eH55pU532JuVAQkLxf5c3dntT7C2uxtetSqvVHYzpI"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/save-fcm-token/",
            json=token_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['message']}")
            return token_data["token"]
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure Django server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_schedule_notification(fcm_token):
    """Test scheduling a notification"""
    print("\n⏰ Testing notification scheduling...")
    
    # Schedule notification for 1 minute from now
    scheduled_time = datetime.now() + timedelta(minutes=1)
    
    notification_data = {
        "title": "🧪 Test Notification",
        "body": "This is a test notification scheduled via API!",
        "fcm_token": fcm_token,
        "scheduled_at": scheduled_time.isoformat(),
        "priority": "high"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/schedule-notification/",
            json=notification_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['message']}")
            print(f"   Notification ID: {result['notification_id']}")
            print(f"   Scheduled for: {result['scheduled_at']}")
            return result['notification_id']
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_get_status():
    """Test getting notification statistics"""
    print("\n📊 Testing status endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/notification-status/")
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print("✅ Statistics retrieved:")
            print(f"   Active Tokens: {data['total_tokens']}")
            print(f"   Total Notifications: {data['total_scheduled']}")
            print(f"   Pending: {data['pending']}")
            print(f"   Sent: {data['sent']}")
            print(f"   Failed: {data['failed']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_check_and_send():
    """Test checking and sending notifications"""
    print("\n🚀 Testing notification processing...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/check-and-send-notifications/")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            if 'sent' in result:
                print(f"   Sent: {result['sent']}")
                print(f"   Failed: {result['failed']}")
                print(f"   Total: {result['total']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🧪 Django Notification System Test")
    print("=" * 40)
    
    # Test 1: Save FCM token
    fcm_token = test_save_fcm_token()
    if not fcm_token:
        print("❌ Cannot proceed without FCM token")
        return
    
    # Test 2: Schedule notification
    notification_id = test_schedule_notification(fcm_token)
    if not notification_id:
        print("❌ Cannot proceed without scheduled notification")
        return
    
    # Test 3: Get status
    test_get_status()
    
    # Test 4: Wait a bit and then check/send
    print("\n⏳ Waiting 2 minutes for scheduled notification to be due...")
    print("   (You can manually trigger this with: python3 manage.py send_scheduled_notifications)")
    
    # Test 5: Check and send notifications
    test_check_and_send()
    
    print("\n🎉 Test completed!")
    print("\nNext steps:")
    print("1. Run: python3 manage.py send_scheduled_notifications")
    print("2. Check the Django admin interface at /admin/")
    print("3. Visit the web interface at /")

if __name__ == "__main__":
    main()
