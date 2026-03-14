import urllib.request
import urllib.error
import json

url = 'https://xstn-website-production.up.railway.app/api/join/'
data = json.dumps({
    'full_name': 'Test User', 
    'email': 'test@example.com', 
    'role': 'Frontend Developer', 
    'message': 'Test'
}).encode('utf-8')

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Origin', 'https://amazing-otter-fe4935.netlify.app')
req.add_header('Content-Type', 'application/json')
req.add_header('Accept', 'application/json')

try:
    res = urllib.request.urlopen(req)
    print('Status:', res.status)
    print(res.read().decode())
except urllib.error.HTTPError as e:
    print('Error Status:', e.code)
    try:
        err_body = e.read().decode()
    except Exception:
        err_body = str(e.read())
    print('Error Body:', err_body[:2000])
