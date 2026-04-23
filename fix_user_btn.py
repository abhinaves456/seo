import sys

with open('index.html', 'r') as f:
    content = f.read()

# Insert the nav-user-btn container into the body
btn_html = '\n<!-- Top User Btn --><div id="nav-user-btn" style="position:fixed;top:env(safe-area-inset-top);right:20px;z-index:500;padding-top:15px;"></div>\n'
content = content.replace('<main id="app"', btn_html + '<main id="app"')

with open('index.html', 'w') as f:
    f.write(content)
