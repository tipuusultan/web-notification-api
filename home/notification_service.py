import json
import time
import base64
import hashlib
import hmac
import requests
from datetime import datetime
from django.conf import settings
import os
import firebase_admin
from firebase_admin import credentials, messaging, exceptions
from django.utils import timezone

class FCMNotificationService:
    """Service to send FCM notifications using Firebase Admin SDK"""
    
    def __init__(self):
        # Use the correct path to static directory
        self.service_account_file = os.path.join(settings.BASE_DIR, 'static', 'service-account.json')
        self.project_id = 'notifications-ed7a5'
        self._initialize_firebase()
        
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if not os.path.exists(self.service_account_file):
                print(f"Service account file not found: {self.service_account_file}")
                return
            
            # Debug: show which credentials file is being used
            try:
                with open(self.service_account_file, 'r') as f:
                    svc = json.load(f)
                print(
                    f"🔎 Using service account: email={svc.get('client_email')} key_id={svc.get('private_key_id')}"
                )
            except Exception as read_err:
                print(f"⚠️ Could not read service account file for debug: {read_err}")

            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.service_account_file)
                # Let SDK infer project ID from service account to avoid mismatches
                firebase_admin.initialize_app(cred)
                print("✅ Firebase Admin SDK initialized successfully")
            else:
                print("✅ Firebase Admin SDK already initialized (existing app retained)")
                
        except Exception as e:
            print(f"❌ Error initializing Firebase: {str(e)}")
    
    def send_notification(self, fcm_token, title, body, priority='high'):
        """Send FCM notification using Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                return {
                    'success': False,
                    'error': 'Firebase not initialized'
                }
            
            # Create notification message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                webpush=messaging.WebpushConfig(
                    notification=messaging.WebpushNotification(
                        icon='https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
                        badge='https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
                        require_interaction=True,
                        vibrate=[200, 100, 200]
                    )
                ),
                android=messaging.AndroidConfig(
                    priority='high' if priority == 'high' else 'normal'
                ),
                token=fcm_token
            )
            
            # Send the message
            response = messaging.send(message)
            
            return {
                'success': True,
                'messageId': response,
                'sent_at': timezone.now()
            }
            
        except messaging.UnregisteredError:
            return {
                'success': False,
                'error': 'FCM token is not registered or invalid'
            }
        except exceptions.InvalidArgumentError as e:
            return {
                'success': False,
                'error': f'Invalid argument: {str(e)}'
            }
        except messaging.QuotaExceededError:
            return {
                'success': False,
                'error': 'Quota exceeded'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global instance
fcm_service = FCMNotificationService()
