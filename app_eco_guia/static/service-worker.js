self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open('eco-guia-cache').then((cache) => {
        return cache.addAll([
          '/',
        //   css -------
          '/static/css/cadastro.css',
          '/static/css/ideias.css',
          '/static/css/index.css',
          '/static/css/scan.css',
          '/static/css/mapa.css',
          '/static/css/update.css',
        //   js ------
          '/static/js/chat.js',
          '/static/js/home.js',
          '/static/js/scan.js',
          '/static/js/mapa.js',
        //   img --------
          '/static/img/artesanato-com-garrafas-de-vidro-1-removebg-preview.png',
          '/static/img/avatar.png',
          '/static/img/favicon.ico',
          '/static/img/COP30.png',
          '/static/img/barcode-scan-icon.png',
          '/static/img/icons8-mensagens-64.png',
          '/static/img/lixoamarelo.png',
          '/static/img/lixoazul-removebg-preview.png',
          '/static/img/lixoverde-removebg-preview.png',
          '/static/img/lixovermelho-removebg-preview.png',
          '/static/img/logotipo.png',
          '/static/img/logotipo2.png',
          '/static/img/portavidro.png',
        //   json ---------
          '/static/dialogos.json',
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  