import sys

with open('index.html', 'r') as f:
    content = f.read()

old_block = """  G.autoMarkers=[];
  firebase.database().ref('drivers').on('value', snap => {
    const drivers = snap.val() || {};
    G.autoMarkers.forEach(m => G.map.removeLayer(m.marker));
    G.autoMarkers = [];
    Object.keys(drivers).forEach(k => {
      const d = drivers[k];
      const icon=L.divIcon({className:'',html:`<div class="auto-dot moving" style="background:var(--accent);"></div>`,iconSize:[10,10],iconAnchor:[5,5]});
      const m=L.marker([d.lat,d.lng],{icon}).addTo(G.map);
      G.autoMarkers.push({id:k,marker:m});
    });
  });"""

new_block = """  G.autoMarkers=[];
  firebase.database().ref('drivers').on('value', snap => {
    const drivers = snap.val() || {};
    const newKeys = Object.keys(drivers);
    // Remove disconnected markers
    for(let i=G.autoMarkers.length-1; i>=0; i--) {
      if(!drivers[G.autoMarkers[i].id]) {
        G.map.removeLayer(G.autoMarkers[i].marker);
        G.autoMarkers.splice(i, 1);
      }
    }
    // Update or add markers
    newKeys.forEach(k => {
      const d = drivers[k];
      const existing = G.autoMarkers.find(m => m.id === k);
      if(existing) {
        existing.marker.setLatLng([d.lat, d.lng]);
      } else {
        const icon=L.divIcon({className:'',html:`<div class="auto-dot moving" style="background:var(--accent);"></div>`,iconSize:[10,10],iconAnchor:[5,5]});
        const m=L.marker([d.lat,d.lng],{icon}).addTo(G.map);
        G.autoMarkers.push({id:k,marker:m});
      }
    });
  });"""

content = content.replace(old_block, new_block)

with open('index.html', 'w') as f:
    f.write(content)
