# 🔔 Web Notification System

A professional Django-based web notification system with Firebase Cloud Messaging (FCM) integration for real-time push notifications.

## 🚀 Features

- **Real-time Push Notifications** using Firebase Cloud Messaging
- **Scheduled Notifications** with automatic processing
- **User Token Management** for multiple devices
- **Professional UI** for notification management
- **Automatic Background Processing** with duplicate prevention
- **Timezone Support** for accurate scheduling

## 📋 Requirements

- Python 3.8+
- Django 4.0+
- Firebase Project with FCM enabled
- Service Account Key from Firebase

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd webNotificationDjango
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your Firebase configuration
```

### 4. Setup Firebase
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Cloud Messaging
3. Download your service account key as `service-account.json`
4. Place it in the `static/` directory
5. Get your VAPID key from Firebase Console

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

## 🚀 Usage

### Start the Development Server
```bash
python manage.py runserver
```

### Start Automatic Notification Processing
```bash
python scripts/simple_auto_fixed.py
```

### Schedule Test Notifications
```bash
python scripts/test_schedule.py
```

### Check for Duplicate Notifications
```bash
python scripts/check_duplicates.py
```

## 📁 Project Structure

```
webNotificationDjango/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables template
├── db.sqlite3                   # SQLite database
├── webNotificationDjango/       # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── home/                        # Main Django app
│   ├── __init__.py
│   ├── admin.py                 # Admin interface
│   ├── apps.py
│   ├── models.py                # Database models
│   ├── views.py                 # View functions
│   ├── urls.py                  # App URL patterns
│   ├── notification_service.py  # Firebase notification service
│   ├── utils.py                 # Utility functions
│   ├── management/              # Django management commands
│   │   └── commands/
│   │       └── send_scheduled_notifications.py
│   └── templates/               # HTML templates
│       └── home/
│           ├── index.html       # Main interface
│           ├── test.html        # Test page
│           ├── simple_test.html # Simple test
│           ├── firebase_test.html # Firebase test
│           └── firebase-messaging-sw.js # Service worker
├── static/                      # Static files
│   ├── service-account.json     # Firebase service account
│   └── firebase-messaging-sw.js # Service worker
├── staticfiles/                 # Collected static files
├── media/                       # User uploads
├── docs/                        # Documentation
│   ├── DUPLICATE_FIX_GUIDE.md
│   ├── PYTHON_ONLY_SOLUTION.md
│   ├── AUTOMATIC_NOTIFICATIONS.md
│   ├── firebase_troubleshooting.md
│   └── get_vapid_key.md
├── scripts/                     # Utility scripts
│   ├── simple_auto_fixed.py     # Main notification processor
│   ├── check_duplicates.py      # Duplicate checker
│   ├── test_schedule.py         # Test notification scheduler
│   ├── schedule_notifications.py # Advanced scheduler
│   └── firebase_config.py       # Firebase configuration
├── tests/                       # Test files
│   └── test_notifications.py
└── templates/                   # Global templates
```

## 🔧 Configuration

### Firebase Configuration
1. **Service Account**: Place your `service-account.json` in the `static/` directory
2. **VAPID Key**: Update the VAPID key in `home/templates/home/index.html`
3. **Firebase Config**: Update Firebase config in the same file

### Environment Variables
Create a `.env` file with:
```env
DEBUG=True
SECRET_KEY=your-secret-key
TIME_ZONE=Asia/Kolkata
```

## 📱 API Endpoints

- `GET /` - Main notification interface
- `POST /api/save-fcm-token/` - Save user FCM token
- `POST /api/schedule-notification/` - Schedule a notification
- `GET /api/check-notifications/` - Check notification status
- `GET /api/timezone-info/` - Get timezone information
- `GET /firebase-messaging-sw.js` - Service worker

## 🔄 Automatic Processing

The system includes an automatic notification processor that:
- Runs continuously in the background
- Checks for due notifications every 60 seconds
- Prevents duplicate sends
- Handles errors gracefully

### Start Automatic Processing
```bash
python scripts/simple_auto_fixed.py
```

## 🧪 Testing

### Test Notifications
```bash
python scripts/test_schedule.py
```

### Check System Health
```bash
python scripts/check_duplicates.py
```

## 📚 Documentation

- [Duplicate Fix Guide](docs/DUPLICATE_FIX_GUIDE.md)
- [Python Only Solution](docs/PYTHON_ONLY_SOLUTION.md)
- [Automatic Notifications](docs/AUTOMATIC_NOTIFICATIONS.md)
- [Firebase Troubleshooting](docs/firebase_troubleshooting.md)
- [Get VAPID Key](docs/get_vapid_key.md)

## 🛡️ Security

- FCM tokens are stored securely
- Service account credentials are protected
- Input validation on all endpoints
- CSRF protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the [documentation](docs/)
2. Review [troubleshooting guide](docs/firebase_troubleshooting.md)
3. Open an issue on GitHub

---

**Built with ❤️ using Django and Firebase**
