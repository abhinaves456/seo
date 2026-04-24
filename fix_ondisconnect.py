import sys

with open('index.html', 'r') as f:
    content = f.read()

old_block = """    const vKey = G.driver.regNo || 'anonymous';
    firebase.database().ref('drivers/' + vKey).set({lat: pos.coords.latitude, lng: pos.coords.longitude});
    firebase.database().ref('drivers/' + vKey).onDisconnect().remove();"""

new_block = """    const vKey = G.driver.regNo || 'anonymous';
    firebase.database().ref('drivers/' + vKey).set({lat: pos.coords.latitude, lng: pos.coords.longitude});
    if(!G.disconnectRegistered) {
      firebase.database().ref('drivers/' + vKey).onDisconnect().remove();
      G.disconnectRegistered = true;
    }"""

content = content.replace(old_block, new_block)

with open('index.html', 'w') as f:
    f.write(content)
