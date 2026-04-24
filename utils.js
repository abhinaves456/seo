const dist=(a,b,c,d)=>{const R=6371,dLat=(c-a)*Math.PI/180,dLng=(d-b)*Math.PI/180,x=Math.sin(dLat/2)**2+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(dLng/2)**2;return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x))};
const distM=(a,b,c,d)=>dist(a,b,c,d)*1000;
const timeAgo=ts=>{const s=Math.floor((Date.now()-ts)/1000);if(s<60)return s+'s ago';const m=Math.floor(s/60);if(m<60)return m+'m ago';return Math.floor(m/60)+'h ago'};
const fmtDist=m=>m<1000?Math.round(m)+'m':(m/1000).toFixed(1)+'km';

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { dist, distM, timeAgo, fmtDist };
}
