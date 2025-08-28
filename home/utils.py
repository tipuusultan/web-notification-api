from datetime import datetime, timedelta, time
from django.utils import timezone
import pytz

def get_current_time():
    """Get current time in your local timezone"""
    return timezone.now()

def schedule_for_local_time(hour, minute, days_ahead=0):
    """
    Schedule a notification for a specific time in your local timezone
    
    Args:
        hour: Hour (0-23)
        minute: Minute (0-59)
        days_ahead: Days from today (0 = today, 1 = tomorrow, etc.)
    
    Returns:
        ISO formatted datetime string
    """
    # Get current date in your timezone
    now = timezone.now()
    
    # Calculate target date
    target_date = now.date() + timedelta(days=days_ahead)
    
    # Create datetime object for the target time
    target_datetime = datetime.combine(target_date, time(hour, minute))
    
    # Make it timezone-aware
    target_datetime = timezone.make_aware(target_datetime)
    
    # If the time has already passed today, schedule for tomorrow
    if days_ahead == 0 and target_datetime <= now:
        target_datetime += timedelta(days=1)
    
    return target_datetime.isoformat()

def schedule_for_minutes_from_now(minutes):
    """
    Schedule a notification for X minutes from now
    
    Args:
        minutes: Minutes from now
    
    Returns:
        ISO formatted datetime string
    """
    future_time = timezone.now() + timedelta(minutes=minutes)
    return future_time.isoformat()

def schedule_for_hours_from_now(hours):
    """
    Schedule a notification for X hours from now
    
    Args:
        hours: Hours from now
    
    Returns:
        ISO formatted datetime string
    """
    future_time = timezone.now() + timedelta(hours=hours)
    return future_time.isoformat()

def schedule_for_daily_time(hour, minute):
    """
    Schedule a daily notification at a specific time
    
    Args:
        hour: Hour (0-23)
        minute: Minute (0-59)
    
    Returns:
        ISO formatted datetime string for next occurrence
    """
    now = timezone.now()
    today = now.date()
    
    # Create time for today
    target_time = datetime.combine(today, time(hour, minute))
    target_time = timezone.make_aware(target_time)
    
    # If time has passed today, schedule for tomorrow
    if target_time <= now:
        target_time += timedelta(days=1)
    
    return target_time.isoformat()

def schedule_for_weekly_time(weekday, hour, minute):
    """
    Schedule a weekly notification on a specific day and time
    
    Args:
        weekday: Day of week (0=Monday, 6=Sunday)
        hour: Hour (0-23)
        minute: Minute (0-59)
    
    Returns:
        ISO formatted datetime string for next occurrence
    """
    now = timezone.now()
    today = now.weekday()
    
    # Calculate days until target weekday
    days_ahead = weekday - today
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    # Calculate target date
    target_date = now.date() + timedelta(days=days_ahead)
    
    # Create datetime object
    target_datetime = datetime.combine(target_date, time(hour, minute))
    target_datetime = timezone.make_aware(target_datetime)
    
    return target_datetime.isoformat()

def format_local_time(datetime_obj):
    """
    Format a datetime object to show in your local timezone
    
    Args:
        datetime_obj: Django timezone-aware datetime
    
    Returns:
        Formatted string in local time
    """
    if timezone.is_naive(datetime_obj):
        datetime_obj = timezone.make_aware(datetime_obj)
    
    return datetime_obj.strftime("%Y-%m-%d %I:%M %p %Z")

def get_timezone_info():
    """
    Get information about current timezone settings
    
    Returns:
        Dictionary with timezone information
    """
    now = timezone.now()
    utc_now = now.utcnow()
    
    return {
        'local_time': now.strftime("%Y-%m-%d %I:%M:%S %p"),
        'utc_time': utc_now.strftime("%Y-%m-%d %I:%M:%S %p"),
        'timezone': str(timezone.get_current_timezone()),
        'offset_hours': int(now.utcoffset().total_seconds() / 3600),
        'is_dst': now.dst() != timedelta(0)
    }
