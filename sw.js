var CACHE = 'coffee-game-v1';
var FILES = ['index.html', 'ar.html', 'ar-gps.html', 'assets/coffee_cup.glb', 'assets/student.glb'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(FILES);
    }).catch(function () {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function (e) {
  var u = new URL(e.request.url);
  if (u.origin !== location.origin) return;
  var path = u.pathname;
  var isOurs = /(index|ar|ar-gps)\.html$/.test(path) || /\/assets\//.test(path);
  if (!isOurs) return;

  e.respondWith(
    fetch(e.request).then(function (r) {
      if (r && r.status === 200) {
        var clone = r.clone();
        caches.open(CACHE).then(function (cache) { cache.put(e.request, clone); });
      }
      return r;
    }).catch(function () {
      return caches.match(e.request);
    })
  );
});
