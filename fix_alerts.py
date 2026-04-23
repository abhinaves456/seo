import sys

with open('index.html', 'r') as f:
    content = f.read()

# Replace the naive STATIONS update block with one that triggers alerts
old_listener = r"""      STATIONS.forEach(s => { if(data[s.id]) { Object.assign(s, data[s.id]); } });"""
new_listener = r"""      STATIONS.forEach(s => {
        if(data[s.id]) {
          const prev = s.status;
          Object.assign(s, data[s.id]);
          if(s.status !== prev && (s.status === 'warn' || s.status === 'busy')) {
            generateAlert(s);
          }
        }
      });"""

content = content.replace(old_listener, new_listener)

with open('index.html', 'w') as f:
    f.write(content)
