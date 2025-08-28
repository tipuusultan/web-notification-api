// Firebase messaging service worker
console.log('Service Worker: Starting...');

// Handle service worker installation
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    self.skipWaiting();
});

// Handle service worker activation
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');
    event.waitUntil(self.clients.claim());
});

// Handle push event (fallback for older browsers)
self.addEventListener('push', (event) => {
    console.log('Service Worker: Push event received:', event);
    
    if (event.data) {
        try {
            const payload = event.data.json();
            const notificationTitle = payload.notification?.title || 'New Notification';
            const notificationOptions = {
                body: payload.notification?.body || 'You have a new notification',
                icon: payload.notification?.icon || 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
                badge: payload.notification?.badge || 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
                tag: 'push-notification-' + Date.now(),
                requireInteraction: true,
                data: payload.data || {}
            };
            
            event.waitUntil(
                self.registration.showNotification(notificationTitle, notificationOptions)
            );
        } catch (error) {
            console.error('Service Worker: Error parsing push data:', error);
            
            // Fallback notification
            const notificationTitle = 'New Notification';
            const notificationOptions = {
                body: 'You have a new notification',
                icon: 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
                tag: 'fallback-notification-' + Date.now()
            };
            
            event.waitUntil(
                self.registration.showNotification(notificationTitle, notificationOptions)
            );
        }
    } else {
        // No data, show default notification
        const notificationTitle = 'New Notification';
        const notificationOptions = {
            body: 'You have a new notification',
            icon: 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
            tag: 'default-notification-' + Date.now()
        };
        
        event.waitUntil(
            self.registration.showNotification(notificationTitle, notificationOptions)
        );
    }
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
    console.log('Service Worker: Notification clicked:', event);
    
    event.notification.close();
    
    // Handle notification click - you can customize this
    if (event.notification.data && event.notification.data.url) {
        event.waitUntil(
            clients.openWindow(event.notification.data.url)
        );
    } else {
        // Default behavior - focus on existing window or open new one
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then((clientList) => {
                if (clientList.length > 0) {
                    clientList[0].focus();
                } else {
                    clients.openWindow('/');
                }
            })
        );
    }
});

// Try to initialize Firebase if available
try {
    importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
    importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');
    
    // Initialize Firebase
    firebase.initializeApp({
        apiKey: "AIzaSyBfk27q_0ybzJWPivChOGATa_w-aDZjIEg",
        authDomain: "notifications-ed7a5.firebaseapp.com",
        projectId: "notifications-ed7a5",
        storageBucket: "notifications-ed7a5.firebasestorage.app",
        messagingSenderId: "63241154363",
        appId: "1:63241154363:web:d6906abe4a5bee83ff911e",
        measurementId: "G-L7NH85PVF6"
    });
    
    // Get messaging instance
    const messaging = firebase.messaging();
    
    // Handle background messages
    messaging.onBackgroundMessage((payload) => {
        console.log('Service Worker: Received background message:', payload);
        
        const notificationTitle = payload.notification.title;
        const notificationOptions = {
            body: payload.notification.body,
            icon: payload.notification.icon || 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
            badge: payload.notification.badge || 'https://cdn-icons-png.flaticon.com/512/3884/3884811.png',
            tag: 'notification-' + Date.now(),
            requireInteraction: true,
            data: payload.data || {}
        };
        
        // Show notification
        self.registration.showNotification(notificationTitle, notificationOptions);
    });
    
    console.log('Service Worker: Firebase initialized successfully');
} catch (error) {
    console.log('Service Worker: Firebase not available, using basic push notifications:', error);
}

console.log('Service Worker: Loaded successfully');
