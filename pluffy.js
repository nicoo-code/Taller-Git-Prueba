(function(window){
  function initMap(targetId){
    const center = [4.5709, -74.2973]; // Colombia centro aproximado
    const map = L.map(targetId).setView(center, 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    L.marker(center).addTo(map).bindPopup('Colombia (centro aproximado)');
    L.circle(center, { radius: 700000, color: '#2E86AB', fillColor:'#2E86AB', fillOpacity:0.08 }).addTo(map);
  }

  window.pluffy = { initMap };
})(window);
