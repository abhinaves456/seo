import sys

with open('index.html', 'r') as f:
    content = f.read()

old_algo_start = '<!-- Algorithm Playground Panel -->\n    <div class="sim-panel" style="pointer-events:auto;width:280px">'
new_algo_start = """<!-- Algorithm Playground Panel -->
    <div id="algo-drawer-handle" onclick="document.getElementById('algo-drawer').classList.toggle('open')" style="position:fixed;bottom:80px;right:20px;width:50px;height:50px;border-radius:25px;background:var(--algo);color:white;display:flex;align-items:center;justify-content:center;z-index:600;box-shadow:0 4px 14px rgba(167,139,250,.4);cursor:pointer;pointer-events:auto;"><i class="fa-solid fa-microchip" style="font-size:20px;"></i></div>
    <div id="algo-drawer" class="sim-panel" style="position:fixed;bottom:0;left:0;width:100%;z-index:700;padding-bottom:calc(10px + env(safe-area-inset-bottom));border-radius:20px 20px 0 0;transform:translateY(100%);transition:transform 0.3s ease-out;pointer-events:auto;box-shadow: 0 -10px 40px rgba(0,0,0,0.5);">
      <button onclick="document.getElementById('algo-drawer').classList.remove('open')" style="position:absolute;top:10px;right:15px;background:none;border:none;color:var(--muted);font-size:20px;cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
"""

content = content.replace(old_algo_start, new_algo_start)

# Ensure CSS rules are updated for open state and sliders
css_addition = "\n#algo-drawer.open { transform: translateY(0) !important; }\n"
if "#algo-drawer.open" not in content:
    content = content.replace('</style>', css_addition + '</style>')

content = content.replace('height:4px;border-radius:2px', 'height:12px;border-radius:6px')
content = content.replace('width:14px;height:14px;border-radius:50%;background:var(--accent);margin-top:-5px;', 'width:28px;height:28px;border-radius:50%;background:var(--accent);margin-top:-8px;')

with open('index.html', 'w') as f:
    f.write(content)
