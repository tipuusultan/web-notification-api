# 🔔 Automatic Notifications Setup Guide

## 🚨 **Why Notifications Don't Send Automatically**

Django doesn't have a built-in task scheduler. Notifications only send when you manually run:
```bash
python3 manage.py send_scheduled_notifications
```

## 🚀 **Solutions for Automatic Notifications**

### **Option 1: Cron Job (✅ Already Set Up!)**

**Status**: ✅ **ACTIVE** - Running every minute

**What's Running**:
```bash
*/1 * * * * cd /Users/tipusultan/Desktop/web-notification-python/webNotificationDjango && python3 manage.py send_scheduled_notifications
```

**Check Status**:
```bash
crontab -l
```

**View Cron Logs**:
```bash
tail -f /var/log/cron
```

### **Option 2: Background Daemon Script**

**Start the daemon**:
```bash
./start_notifications.sh
```

**Check daemon status**:
```bash
tail -f daemon.log
```

**Stop the daemon**:
```bash
pkill -f run_notifications_daemon.py
```

**Manual daemon start**:
```bash
python3 run_notifications_daemon.py
```

### **Option 3: macOS LaunchAgent (Automatic Startup)**

**Install LaunchAgent**:
```bash
# Copy the plist file to LaunchAgents directory
cp com.notification.daemon.plist ~/Library/LaunchAgents/

# Load the service
launchctl load ~/Library/LaunchAgents/com.notification.daemon.plist

# Start the service
launchctl start com.notification.daemon
```

**Uninstall LaunchAgent**:
```bash
launchctl unload ~/Library/LaunchAgents/com.notification.daemon.plist
rm ~/Library/LaunchAgents/com.notification.daemon.plist
```

### **Option 4: Simple Background Loop**

**Start continuous processing**:
```bash
while true; do 
    python3 manage.py send_scheduled_notifications
    sleep 60  # Wait 1 minute
done
```

**Stop the loop**: Press `Ctrl+C`

## 🧪 **Test Automatic Notifications**

### **Step 1: Schedule a Test Notification**
```bash
python3 test_schedule.py
```

### **Step 2: Wait for Automatic Processing**
The cron job will automatically process it within 1 minute.

### **Step 3: Check Results**
```bash
# Check notification status
python3 manage.py shell -c "from home.models import ScheduledNotification; print('Pending:', ScheduledNotification.objects.filter(status='pending').count()); print('Sent:', ScheduledNotification.objects.filter(status='sent').count())"

# Check daemon logs (if using daemon)
tail -f daemon.log
```

## 📊 **Monitoring Automatic Notifications**

### **Check Cron Job Status**
```bash
# View cron jobs
crontab -l

# Check cron logs
tail -f /var/log/cron

# Check if cron is running
ps aux | grep cron
```

### **Check Daemon Status**
```bash
# Check if daemon is running
ps aux | grep run_notifications_daemon.py

# View daemon logs
tail -f daemon.log

# Check daemon process
pgrep -f run_notifications_daemon.py
```

### **Check Notification Status**
```bash
# API endpoint
curl http://127.0.0.1:8000/api/notification-status/

# Django admin
# Visit: http://127.0.0.1:8000/admin/
```

## 🔧 **Troubleshooting**

### **Cron Job Not Working**
```bash
# Check cron service
sudo launchctl list | grep cron

# Restart cron
sudo launchctl unload /System/Library/LaunchDaemons/com.vix.cron.plist
sudo launchctl load /System/Library/LaunchDaemons/com.vix.cron.plist
```

### **Daemon Not Working**
```bash
# Check daemon process
ps aux | grep run_notifications_daemon.py

# Restart daemon
pkill -f run_notifications_daemon.py
./start_notifications.sh
```

### **Notifications Still Not Sending**
```bash
# Check if there are due notifications
python3 manage.py shell -c "from home.models import ScheduledNotification; from django.utils import timezone; now = timezone.now(); due = ScheduledNotification.objects.filter(status='pending', scheduled_at__lte=now); print('Due notifications:', due.count())"

# Test manual processing
python3 manage.py send_scheduled_notifications
```

## 🎯 **Recommended Setup**

### **For Development/Testing**:
- ✅ **Cron Job** (already active)
- ✅ **Manual testing** with `test_schedule.py`

### **For Production**:
- ✅ **Cron Job** (reliable, simple)
- 🔄 **Daemon Script** (more control, logging)
- 🔄 **Systemd Service** (Linux servers)

### **For macOS Desktop**:
- ✅ **Cron Job** (already active)
- 🔄 **LaunchAgent** (starts automatically on boot)

## 📱 **Current Status**

- ✅ **Cron job active** - checking every minute
- ✅ **Firebase Admin SDK working**
- ✅ **Notifications being sent automatically**
- ✅ **Timezone properly configured (IST)**

## 🚀 **Next Steps**

1. **Test automatic notifications**:
   ```bash
   python3 test_schedule.py
   # Wait 1-2 minutes for automatic processing
   ```

2. **Monitor the system**:
   ```bash
   tail -f /var/log/cron  # Cron logs
   tail -f daemon.log      # Daemon logs (if using)
   ```

3. **Schedule real notifications**:
   ```bash
   python3 schedule_notifications.py
   ```

4. **Set up monitoring** (optional):
   - Email alerts for failed notifications
   - Dashboard for notification statistics
   - Health checks for the daemon

## 🆘 **Need Help?**

- **Check logs**: `tail -f daemon.log`
- **Test manually**: `python3 manage.py send_scheduled_notifications`
- **Verify cron**: `crontab -l`
- **Check process**: `ps aux | grep notification`

Your notifications are now **fully automatic**! 🎉
