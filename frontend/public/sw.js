const CACHE_NAME = "pathpilot-v1";
const STATIC_ASSETS = [
  "/",
  "/manifest.json",
  "/styles/globals.css",
  "/lib/translations.ts",
  "/icons/icon-192.png",
  "/icons/icon-512.png"
];

// Installs service worker and caches core layouts
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Static caching initialized successfully.");
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        // Safe bypass if any specific asset is not compiled yet during build
        console.warn("Some assets missed in pre-cache:", err);
      });
    })
  );
  self.skipWaiting();
});

// Activating service worker and pruning legacy storage keys
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Dynamic cache fallback proxy interceptor
self.addEventListener("fetch", (event) => {
  // Only handle standard HTTP/HTTPS schemes
  if (!event.request.url.startsWith("http")) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      
      return fetch(event.request)
        .then((networkResponse) => {
          // If response is valid, clone and cache it dynamically for subsequent offline load
          if (
            networkResponse && 
            networkResponse.status === 200 && 
            event.request.method === "GET"
          ) {
            const cacheCopy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, cacheCopy);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Fetch fails (e.g. offline). Return offline fallback shell if navigating page
          if (event.request.mode === "navigate") {
            return caches.match("/");
          }
          return new Response(
            JSON.stringify({ error: "Offline network connection interrupted." }),
            { headers: { "Content-Type": "application/json" } }
          );
        });
    })
  );
});
