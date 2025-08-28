# How to Get Your VAPID Key from Firebase

## Step-by-Step Instructions:

1. **Go to Firebase Console**
   - Visit: https://console.firebase.google.com/
   - Select your project: `notifications-ed7a5`

2. **Navigate to Project Settings**
   - Click the gear icon (⚙️) next to "Project Overview"
   - Select "Project settings"

3. **Go to Cloud Messaging Tab**
   - Click on the "Cloud Messaging" tab
   - Scroll down to "Web configuration" section

4. **Generate VAPID Key Pair**
   - If you don't see a key pair, click "Generate key pair"
   - Copy the generated "Key pair" value

5. **Update Your Code**
   - Replace `YOUR_VAPID_KEY_HERE` in `home/templates/home/index.html`
   - The VAPID key should look like: `BEl62iGZ...` (long string)

## Example:
```javascript
fcmToken = await messaging.getToken({
    vapidKey: 'BEl62iGZ...' // Your actual VAPID key here
});
```

## Important Notes:
- The VAPID key is required for web push notifications
- Keep it secure but it's safe to include in client-side code
- The same key can be used for all users of your app
- If you regenerate the key, existing subscriptions will stop working

## Troubleshooting:
- If you don't see the Cloud Messaging tab, make sure you have the right permissions
- If you can't generate a key, check that you're the project owner or have admin rights
- Make sure your project has the Blaze (pay-as-you-go) plan if you're using FCM
