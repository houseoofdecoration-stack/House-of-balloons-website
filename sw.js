/* images: cache-first for faster repeat visits; page/sync.js always from network (owner edits stay live) */
const C='hob-img-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin||!/\/img\/.+\.(jpg|png|webp)$/.test(u.pathname))return;
  e.respondWith(caches.open(C).then(c=>c.match(e.request).then(h=>h||fetch(e.request).then(r=>{if(r.ok)c.put(e.request,r.clone());return r}))));
});
