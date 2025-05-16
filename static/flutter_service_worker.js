'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"flutter_bootstrap.js": "f6c7c1ce395a58115d39776b3bb5bbbb",
"version.json": "1a5d1f7a4cdca5cf9b4c9d6c16773bc6",
"index.html": "2a029de9cfa6b8034f7b513f090bd87f",
"/": "2a029de9cfa6b8034f7b513f090bd87f",
"main.dart.js": "caf9636575c0be32356abbbc81eea341",
"flutter.js": "4b2350e14c6650ba82871f60906437ea",
"favicon.png": "7b8ead1aa3012b9199202808a14b1077",
"icons/Icon-192.png": "030f8e3c80ae5daba4d16db3c3d84894",
"icons/Icon-maskable-192.png": "030f8e3c80ae5daba4d16db3c3d84894",
"icons/Icon-maskable-512.png": "d4c5c3483aa783c91f467c9e3fe12564",
"icons/Icon-512.png": "d4c5c3483aa783c91f467c9e3fe12564",
"manifest.json": "ebaff07e53e06016badf081c07362919",
"assets/AssetManifest.json": "8395dda728453a13bf0c0354246786de",
"assets/NOTICES": "3b94e232d27d7b686601b43c0941f6ea",
"assets/FontManifest.json": "dc3d03800ccca4601324923c0b1d6d57",
"assets/AssetManifest.bin.json": "42ccd9e6c8f12376aaec0b6c54861cda",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "e986ebe42ef785b27164c36a9abc7818",
"assets/shaders/ink_sparkle.frag": "ecc85a2e95f5e9f53123dcaf8cb9b6ce",
"assets/AssetManifest.bin": "d32d80ada15ed3620e8121903cd9bc45",
"assets/fonts/MaterialIcons-Regular.otf": "d1813688f9d6735f87a294f441a5584c",
"assets/assets/ipcf.png": "d6139d0f8a6e3adc11c2e6ac89c6e1c2",
"assets/assets/privacyPolicyEng.md": "1749074b7b49d16f609778bbaf47f15f",
"assets/assets/instructionsVideoItaDesktop.mp4": "5e58fc82447b209469ad08a8a3a26134",
"assets/assets/privacyPolicyIta.md": "a20148b1d12a0076ca50912a160a7910",
"assets/assets/startLabelingProcessIta.md": "021666c015a0c60d40e6b27e7510eeee",
"assets/assets/instructionsIta.md": "f3b326392ea4230e84d53e7043921d4e",
"assets/assets/cnr.png": "85be9da04fb90987a2eaf6bf54d13275",
"assets/assets/instructionsVideoEngMobile.mp4": "053fdcdca107f183d45f568e6e20f337",
"assets/assets/disclaimerEmailIta.md": "7ffbac34e6b8441b53d16fcb0bfe3d70",
"assets/assets/instructionsEng.md": "984d83d1e17b003485035654c804f10a",
"assets/assets/startLabelingProcessEng.md": "19eae927d9f8c8fcddffc917cf896330",
"assets/assets/disclaimerEmailEng.md": "eabd5bae75824f5ad6d917e019154fb5",
"assets/assets/cnripcf.png": "746771ff1d758672a564b9987e4545e5",
"assets/assets/disclaimersIta.md": "b3fa94fdc9664a9e77e4fbf087b12b8f",
"assets/assets/instructionsVideoEngDesktop.mp4": "615a3dcb0ce66bdab9d3cdc6ddba7072",
"assets/assets/disclaimersEng.md": "c21b59675b9c19fbf96435fb5deaff5b",
"assets/assets/instructionsVideoItaMobile.mp4": "bc3ce5996a428b163481c2ffd584f78c",
"assets/assets/sedicon.png": "d0322fbaf1eab7fdec76357f8b186cd3",
"canvaskit/skwasm.js": "ac0f73826b925320a1e9b0d3fd7da61c",
"canvaskit/skwasm.js.symbols": "48f5755fe41624ab333ee4285fab9022",
"canvaskit/canvaskit.js.symbols": "d1ee6ccd3369a12d3ddd1a7d35b4e513",
"canvaskit/skwasm.wasm": "012cfa9b9f18943691bb4e2cd4f9de74",
"canvaskit/chromium/canvaskit.js.symbols": "e3dc58952b91cdfaac8c98eb2a77e1fd",
"canvaskit/chromium/canvaskit.js": "b7ba6d908089f706772b2007c37e6da4",
"canvaskit/chromium/canvaskit.wasm": "8e5f40aee64234152cbcc993538b82ce",
"canvaskit/canvaskit.js": "26eef3024dbc64886b7f48e1b6fb05cf",
"canvaskit/canvaskit.wasm": "5c49861614637956a5f2f6439a619dd6",
"canvaskit/skwasm.worker.js": "89990e8c92bcb123999aa81f7e203b1c"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"flutter_bootstrap.js",
"assets/AssetManifest.bin.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
