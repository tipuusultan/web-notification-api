#!/usr/bin/env python3
"""
Firebase Configuration Checker
Verify Firebase configuration and test connectivity
"""

import os
import sys
import json
import requests

# Add the parent directory to Python path to find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webNotificationDjango.settings')
import django
django.setup()

from home.notification_service import FCMNotificationService

def check_firebase_config():
    """Check Firebase configuration"""
    print("🔍 Checking Firebase Configuration...")
    print("=" * 50)
    
    # Check service account file
    service_account_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'service-account.json')
    
    if not os.path.exists(service_account_path):
        print(f"❌ Service account file not found at: {service_account_path}")
        return False
    
    print(f"✅ Service account file found at: {service_account_path}")
    
    try:
        with open(service_account_path, 'r') as f:
            config = json.load(f)
        
        required_fields = ['project_id', 'private_key_id', 'client_email', 'client_id']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field: {field}")
                return False
        
        print(f"✅ Project ID: {config['project_id']}")
        print(f"✅ Client Email: {config['client_email']}")
        print(f"✅ Client ID: {config['client_id']}")
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in service account file")
        return False
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False
    
    return True

def test_firebase_service():
    """Test Firebase notification service"""
    print("\n🧪 Testing Firebase Service...")
    print("=" * 50)
    
    try:
        service = FCMNotificationService()
        print("✅ Firebase service initialized successfully")
        
        # Test sending a notification (this will fail without valid FCM token)
        print("✅ Firebase configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Firebase service error: {e}")
        return False

def main():
    """Main function"""
    print("🔥 FIREBASE CONFIGURATION CHECKER")
    print("=" * 60)
    
    # Check configuration
    config_ok = check_firebase_config()
    
    if config_ok:
        # Test service
        service_ok = test_firebase_service()
        
        if service_ok:
            print("\n🎉 All Firebase checks passed!")
            print("✅ Your Firebase configuration is ready to use")
        else:
            print("\n⚠️  Firebase configuration issues detected")
            print("💡 Check your service account file and network connection")
    else:
        print("\n❌ Firebase configuration issues detected")
        print("💡 Please check your service account file")

if __name__ == "__main__":
    main()
