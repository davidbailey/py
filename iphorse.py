import requests

r = requests.get('http://iphorse.com/json.php')
r.json()['remote_addr']
