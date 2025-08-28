from django.contrib import admin
from .models import UserFCMToken, ScheduledNotification

@admin.register(UserFCMToken)
class UserFCMTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('token',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ScheduledNotification)
class ScheduledNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'fcm_token', 'scheduled_at', 'priority', 'status', 'sent_at')
    list_filter = ('status', 'priority', 'scheduled_at', 'created_at')
    search_fields = ('title', 'body')
    readonly_fields = ('created_at', 'sent_at')
    date_hierarchy = 'scheduled_at'
