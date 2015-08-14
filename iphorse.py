import requests
import json

r = requests.get('http://iphorse.com/json.php')
json.loads(r.text)['remote_addr']
