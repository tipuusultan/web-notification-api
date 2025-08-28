from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test_page, name='test_page'),
    path('simple/', views.simple_test, name='simple_test'),
    path('firebase/', views.firebase_test, name='firebase_test'),
    path('firebase-messaging-sw.js', views.service_worker, name='service_worker'),
    path('api/save-fcm-token/', views.save_fcm_token, name='save_fcm_token'),
    path('api/schedule-notification/', views.schedule_notification, name='schedule_notification'),
    path('api/check-and-send-notifications/', views.check_and_send_notifications, name='check_and_send_notifications'),
    path('api/notification-status/', views.get_notification_status, name='notification_status'),
    path('api/timezone-info/', views.get_timezone_info, name='timezone_info'),
    path('send/', views.send_notification, name='send_notification'),  # Legacy endpoint
]
