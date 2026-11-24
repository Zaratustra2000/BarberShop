// Mapas Leaflet + OpenStreetMap. Lê a configuração dos atributos data-*.
(function () {
  var CENTRO_PADRAO = [-22.951, -43.184]; // Botafogo, público do Canvas MVP

  function base(el, centro, zoom) {
    var mapa = L.map(el).setView(centro, zoom);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap"
    }).addTo(mapa);
    return mapa;
  }

  // <div data-mapa-seletor data-lat="#lat" data-lng="#lng">: clique marca o ponto.
  document.querySelectorAll("[data-mapa-seletor]").forEach(function (el) {
    var lat = document.querySelector(el.dataset.lat);
    var lng = document.querySelector(el.dataset.lng);
    var mapa = base(el, CENTRO_PADRAO, 14);
    var marcador = null;
    mapa.on("click", function (e) {
      lat.value = e.latlng.lat.toFixed(6);
      lng.value = e.latlng.lng.toFixed(6);
      if (marcador) { marcador.setLatLng(e.latlng); }
      else { marcador = L.marker(e.latlng).addTo(mapa); }
    });
  });

  // <div data-mapa-marcadores='[{"lat":..,"lng":..,"titulo":".."}]'>
  document.querySelectorAll("[data-mapa-marcadores]").forEach(function (el) {
    var pontos = JSON.parse(el.dataset.mapaMarcadores || "[]");
    var mapa = base(el, CENTRO_PADRAO, 13);
    var limites = [];
    pontos.forEach(function (p) {
      var m = L.marker([p.lat, p.lng]).addTo(mapa);
      var caixa = document.createElement("div");
      var titulo = document.createElement("strong");
      titulo.textContent = p.titulo;
      caixa.appendChild(titulo);
      if (p.detalhe) {
        caixa.appendChild(document.createElement("br"));
        caixa.appendChild(document.createTextNode(p.detalhe));
      }
      m.bindPopup(caixa);
      limites.push([p.lat, p.lng]);
    });
    if (limites.length) { mapa.fitBounds(limites, { maxZoom: 15, padding: [30, 30] }); }
  });
})();
