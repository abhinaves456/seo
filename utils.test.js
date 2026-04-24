const assert = require('assert');
const { dist } = require('./utils');

describe('dist (Haversine distance)', () => {
  it('should return 0 for the same point', () => {
    const lat = 12.9716;
    const lng = 77.5946;
    assert.strictEqual(dist(lat, lng, lat, lng), 0);
  });

  it('should correctly calculate distance between two points (Bangalore to Mumbai)', () => {
    // Bangalore: 12.9716, 77.5946
    // Mumbai: 19.0760, 72.8777
    // Distance is approximately 840-850 km
    const d = dist(12.9716, 77.5946, 19.0760, 72.8777);
    assert.ok(d > 840 && d < 850, `Distance ${d} km should be between 840 and 850 km`);
  });

  it('should be symmetric', () => {
    const lat1 = 12.9716, lng1 = 77.5946;
    const lat2 = 13.0373, lng2 = 77.5961;
    assert.strictEqual(dist(lat1, lng1, lat2, lng2), dist(lat2, lng2, lat1, lng1));
  });

  it('should handle small distances', () => {
    const lat1 = 12.9716, lng1 = 77.5946;
    const lat2 = 12.9717, lng2 = 77.5946; // approx 11 meters
    const d = dist(lat1, lng1, lat2, lng2);
    assert.ok(d > 0.01 && d < 0.012, `Distance ${d} should be around 0.011 km`);
  });
});
