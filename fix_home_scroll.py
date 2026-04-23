import sys

with open('index.html', 'r') as f:
    content = f.read()

# Instead of calling renderHome() which destroys the DOM, we can call a lighter function,
# or simply let updateStatsBar() run. Wait, if the user specifically asked for real-time station cards on home,
# the original code didn't even have swipeable rows, so it was fine to re-render.
# Now with swipeable rows, a re-render resets scroll.
# I'll replace `if(G.currentPage === 'home') renderHome(document.getElementById('app'));`
# with a targeted update function.
old_call = "if(G.currentPage === 'home') renderHome(document.getElementById('app'));"

new_call = """if(G.currentPage === 'home') {
        STATIONS.forEach(s => {
          const qEl = document.getElementById('home-q-' + s.id);
          const pEl = document.getElementById('home-p-' + s.id);
          if(qEl) qEl.innerText = s.queue + ' waiting';
          if(pEl) {
            pEl.className = 'pill ' + (s.status==='ok'?'pill-ok':s.status==='warn'?'pill-warn':'pill-danger');
            pEl.innerText = s.status==='ok'?'Available':s.status==='warn'?'Moderate':'Busy';
          }
        });
      }"""

content = content.replace(old_call, new_call)

# Now I need to make sure renderHome actually attaches those IDs
def modify_render_home(c):
    start = c.find('function renderHome(el){')
    if start == -1: return c
    end = c.find('}', start)
    block = c[start:end]

    block = block.replace('<span class="pill ${pillCls[s.status]}">${lbl[s.status]}</span>', '<span id="home-p-${s.id}" class="pill ${pillCls[s.status]}">${lbl[s.status]}</span>')
    block = block.replace('<span style="font-size:12px;color:var(--muted)"><i class="fa-solid fa-car" style="margin-right:5px"></i>${s.queue} waiting</span>', '<span id="home-q-${s.id}" style="font-size:12px;color:var(--muted)"><i class="fa-solid fa-car" style="margin-right:5px"></i>${s.queue} waiting</span>')

    return c[:start] + block + c[end:]

content = modify_render_home(content)

with open('index.html', 'w') as f:
    f.write(content)
