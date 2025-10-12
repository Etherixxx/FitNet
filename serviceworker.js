const CACHE_NAME = "fitnet-cache-v1";
const urlsToCache = [
  '/',
  '/dashboard',
  '/log-workout',
  '/progress', 
  '/profile',
  'static/css/dashboard.css',
  'static/js/log-workout.js',
  'static/js/progress.js',
  'static/images/FitNet Logo.png',
  'static/favicon/favicon.ico',
  'static/favicon/favicon-16x16.png',
  'static/favicon/favicon-32x32.png',
  'static/favicon/favicon-96x96.png',
  'static/favicon/web-app-manifest-192x192.png',
  'static/favicon/web-app-manifest-512x512.png',
  'static/favicon/apple-touch-icon.png',
  'manifest.json'
];

// install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// fetch event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => {
        if (event.request.destination === 'document') {
          return caches.match('/dashboard');
        }
        return new Response('Offline - Content not available');
      })
  );
});

// activate event
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});
});
