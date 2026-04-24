import sys

with open('index.html', 'r') as f:
    content = f.read()

content = content.replace(
    'firebase.initializeApp({\n    databaseURL: "https://lpg-smartroute-default-rtdb.firebaseio.com"\n  });',
    'firebase.initializeApp({apiKey: "YOUR_API_KEY", databaseURL: "YOUR_DATABASE_URL", projectId: "YOUR_PROJECT_ID"});'
)

with open('index.html', 'w') as f:
    f.write(content)
