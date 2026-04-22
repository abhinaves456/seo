const CACHE_NAME = "lpg-app-v1";
const urlsToCache = [
  "/seo/",
  "/seo/index.html",
  "/seo/manifest.json",
  "/seo/icon-192.png",
  "/seo/icon-512.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});