// MC Chris — Service Worker (minimal, für PWA-Installability)
const CACHE = 'mc-chris-v1';
const ASSETS = ['/m', '/manifest.webmanifest', '/mc-icon-192.png', '/mc-icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // Network-first: immer frisch vom Server, nur bei Offline auf Cache fallen
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
