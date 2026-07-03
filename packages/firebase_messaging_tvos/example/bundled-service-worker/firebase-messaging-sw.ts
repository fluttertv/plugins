import { initializeApp } from 'firebase/app';
import {
  experimentalSetDeliveryMetricsExportedToBigQueryEnabled,
  getMessaging,
  isSupported,
  onBackgroundMessage
} from 'firebase/messaging/sw';

declare var self: ServiceWorkerGlobalScope;

self.addEventListener('install', (event) => {
  console.log(self);
  console.log(event);
});

// Focus the existing app tab when a notification is clicked.
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients
      .matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        for (const client of clientList) {
          if (!client.focused) {
            return client.focus();
          }
        }
      })
  );
});

const app = initializeApp({
  apiKey: 'YOUR_API_KEY',
  appId: 'YOUR_APP_ID',
  messagingSenderId: 'YOUR_SENDER_ID',
  projectId: 'your-project-id',
  authDomain: 'your-project-id.firebaseapp.com',
  databaseURL:
      'https://your-project-id-default-rtdb.europe-west1.firebasedatabase.app',
  storageBucket: 'your-project-id.appspot.com',
  measurementId: 'YOUR_MEASUREMENT_ID',
});

isSupported().then((isSupported) => {
  if (isSupported) {
    const messaging = getMessaging(app);

    experimentalSetDeliveryMetricsExportedToBigQueryEnabled(messaging, true);

    onBackgroundMessage(messaging, ({ notification: notification }) => {
      const { title, body, image } = notification ?? {};

      if (!title) {
        return;
      }

      self.registration.showNotification(title, {
        body,
        icon: image || '/assets/icons/icon-72x72.png',
      });
    });
  }
});
