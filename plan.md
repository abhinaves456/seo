1. **Fix Missing Logout/User Button**
   - Add `<div id="nav-user-btn"></div>` back into the app, possibly at the top of the `#dashboard` view or as part of the bottom navigation or a new small top header (the prompt allows bottom nav instead of top navbar, but we still need the user button. I'll put it at the top of the dashboard or home, or simply restore a minimal top header for it since the original code dynamically rendered it there). Actually, placing it in the `renderDashboard` or a small top-right floating button is best. I will add it back to a top floating container.

2. **Fix Alerts Generation**
   - In the Firebase `on('value')` listener for `stations`, I need to restore the logic that checks if the status changed to `warn` or `busy` and calls `generateAlert(s)`.

3. **Fix `onDisconnect` spam**
   - Only call `firebase.database().ref('drivers/' + vKey).onDisconnect().remove()` ONCE, e.g., using a flag `if(!G.disconnectRegistered) { ... G.disconnectRegistered = true; }`.

4. **Fix Map Markers Performance**
   - Update `initMap` to not destroy markers. Instead, check if the marker exists in `G.autoMarkers`. If yes, call `setLatLng([d.lat, d.lng])`. If no, create it. Iterate and remove any markers for keys that no longer exist in the snapshot.

5. **Fix Unusable UI Scroll-State on Home**
   - The Firebase listener calls `renderHome(document.getElementById('app'))`. Instead of doing this, I should just call `updateStatsBar()` and a new function `updateHomeData()` that updates the DOM nodes (like `innerText` of queue counts) directly, or just avoid calling `renderHome` on every tick. The original code did `if(G.currentPage==='home') renderHome()`. Wait, the original code DID do this! Let me check `simTick()`. Actually, `simTick` did `renderApp()`? Let me look at the original interval. I'll modify the Firebase listener to only call a specific UI update function for the queues or disable the full re-render.

6. **Fix Algorithm Playground**
   - The prompt says: "The algorithm playground becomes a bottom drawer with large touch sliders." I will find the algorithm playground HTML (`<!-- Algorithm Playground Panel -->`) and style it as a bottom drawer (`position: fixed; bottom: 0; left: 0; width: 100%; z-index: 500; transform: translateY(100%); transition: transform...`) with a toggle button to slide it up.

7. **Request Code Review**
   - Request final review.

8. **Submit**
   - Submit the code.
