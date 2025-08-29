// notification-auto-scheduler.js
// Automatically handles notification scheduling when page loads

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBfk27q_0ybzJWPivChOGATa_w-aDZjIEg",
    authDomain: "notifications-ed7a5.firebaseapp.com",
    projectId: "notifications-ed7a5",
    storageBucket: "notifications-ed7a5.firebasestorage.app",
    messagingSenderId: "63241154363",
    appId: "1:63241154363:web:d6906abe4a5bee83ff911e",
    measurementId: "G-L7NH85PVF6"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Global variable to store FCM token
let fcmToken = null;

// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// Auto-initialize when page loads
document.addEventListener('DOMContentLoaded', async function() {
    console.log('Page loaded - starting automatic notification setup...');
    
    // Check browser support
    if (!('Notification' in window)) {
        console.error('This browser does not support notifications');
        return;
    }
    
    if (!('serviceWorker' in navigator)) {
        console.error('Service Worker is not supported in this browser');
        return;
    }
    
    // Start the automatic process
    await initializeNotificationSystem();
});

// Main initialization function
async function initializeNotificationSystem() {
    try {
        // Step 1: Request notification permission
        console.log('Step 1: Requesting notification permission...');
        const permission = await Notification.requestPermission();
        
        if (permission !== 'granted') {
            console.error('Notification permission denied or dismissed');
            alert('Please allow notifications to continue');
            return;
        }
        
        console.log('Notification permission granted');
        
        // Step 2: Initialize FCM and get token
        console.log('Step 2: Initializing FCM...');
        const token = await initializeFCM();
        
        if (!token) {
            console.error('Failed to get FCM token');
            return;
        }
        
        // Step 3: Save token to database
        console.log('Step 3: Saving FCM token to database...');
        const tokenSaved = await saveFCMToken(token);
        
        if (!tokenSaved) {
            console.error('Failed to save token to database');
            return;
        }
        
        // Step 4: Get date and time from page and schedule notification
        console.log('Step 4: Scheduling notification from page data...');
        await scheduleNotificationFromPage();
        
    } catch (error) {
        console.error('Error in initialization:', error);
        alert('Error setting up notifications: ' + error.message);
    }
}

// Initialize Firebase Cloud Messaging
async function initializeFCM() {
    try {
        // Register service worker
        const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
        console.log('Service Worker registered');
        
        // Wait for service worker to be ready
        await navigator.serviceWorker.ready;
        
        // Get FCM token
        const messaging = firebase.messaging();
        fcmToken = await messaging.getToken({
            vapidKey: 'BBj2Oj74z-Yl4MUQYJSoltNFCV2fmBrodGqkVUVLs7bihSP0XitjLOqwEFDCysP2X9mOdbZRkBP79l21qbXsdVg'
        });
        
        if (fcmToken) {
            console.log('FCM token received:', fcmToken);
            return fcmToken;
        } else {
            console.error('No FCM token received');
            return null;
        }
    } catch (error) {
        console.error('Error initializing FCM:', error);
        return null;
    }
}

// Save FCM token to server
async function saveFCMToken(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/save-fcm-token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token: token })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('FCM token saved to database successfully');
            return true;
        } else {
            console.error('Server error saving token:', result.error);
            return false;
        }
    } catch (error) {
        console.error('Network error saving token:', error);
        return false;
    }
}

// Get date and time from page spans and schedule notification
async function scheduleNotificationFromPage() {
    try {
        // Get date and time from span elements
        const dateSpan = document.getElementById('date');
        const timeSpan = document.getElementById('time');
        
        if (!dateSpan || !timeSpan) {
            console.error('Date or time span not found on page');
            alert('Cannot find date or time information on the page');
            return false;
        }
        
        const dateText = dateSpan.textContent.trim();
        const timeText = timeSpan.textContent.trim();
        
        console.log('Date from page:', dateText);
        console.log('Time from page:', timeText);
        
        if (!dateText || !timeText) {
            console.error('Date or time is empty');
            alert('Date or time information is missing');
            return false;
        }
        
        // Parse and combine date and time
        // Assuming date is in format like "2025-01-15" or "15/01/2025" or "January 15, 2025"
        // and time is in format like "14:30" or "2:30 PM"
        let scheduledDateTime;
        
        try {
            // Try to parse the date and time
            // First, try combining as is
            scheduledDateTime = new Date(`${dateText} ${timeText}`);
            
            // If invalid, try different formats
            if (isNaN(scheduledDateTime.getTime())) {
                // Try ISO format
                scheduledDateTime = new Date(`${dateText}T${timeText}`);
            }
            
            // If still invalid, try parsing separately
            if (isNaN(scheduledDateTime.getTime())) {
                const datePart = new Date(dateText);
                const timeParts = timeText.match(/(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
                
                if (timeParts) {
                    let hours = parseInt(timeParts[1]);
                    const minutes = parseInt(timeParts[2]);
                    const period = timeParts[3];
                    
                    if (period && period.toUpperCase() === 'PM' && hours !== 12) {
                        hours += 12;
                    } else if (period && period.toUpperCase() === 'AM' && hours === 12) {
                        hours = 0;
                    }
                    
                    datePart.setHours(hours, minutes, 0, 0);
                    scheduledDateTime = datePart;
                }
            }
            
        } catch (parseError) {
            console.error('Error parsing date/time:', parseError);
            alert('Could not parse the date and time from the page');
            return false;
        }
        
        // Validate the parsed date
        if (isNaN(scheduledDateTime.getTime())) {
            console.error('Invalid date/time after parsing');
            alert('Invalid date or time format on the page');
            return false;
        }
        
        // Check if date is in the future
        if (scheduledDateTime <= new Date()) {
            console.warn('Scheduled time is in the past, adding 24 hours');
            scheduledDateTime = new Date(scheduledDateTime.getTime() + 24 * 60 * 60 * 1000);
        }
        
        console.log('Scheduled DateTime:', scheduledDateTime.toISOString());
        
        // Schedule the notification
        const response = await fetch(`${API_BASE_URL}/api/schedule-notification/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: '🔔 Scheduled Reminder',
                body: `Your scheduled notification for ${scheduledDateTime.toLocaleString()}`,
                fcm_token: fcmToken,
                scheduled_at: scheduledDateTime.toISOString(),
                priority: 'high'
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Notification scheduled successfully');
            alert(`✅ Notification scheduled for ${scheduledDateTime.toLocaleString()}`);
            
            // Show success message on page if there's an element for it
            const statusElement = document.getElementById('notification-status');
            if (statusElement) {
                statusElement.textContent = `Notification scheduled for ${scheduledDateTime.toLocaleString()}`;
                statusElement.style.color = 'green';
            }
            
            return true;
        } else {
            console.error('Failed to schedule notification:', result.error);
            alert('Failed to schedule notification: ' + result.error);
            return false;
        }
        
    } catch (error) {
        console.error('Error scheduling notification:', error);
        alert('Error scheduling notification: ' + error.message);
        return false;
    }
}

// Helper function to manually trigger the process (optional)
window.initializeNotifications = initializeNotificationSystem;