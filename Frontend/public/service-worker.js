self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/manifest.json',
        '/src/js/main.js',
        '/src/js/router.js',
        '/src/css/styles.css'
        // Ajouter d'autres fichiers si besoin
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => {
      return resp || fetch(event.request);
    })
  );
});
