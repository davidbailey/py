import requests

r = requests.get('http://iphorse.com/json.php')
r.json()['remote_addr']

import yaml
print yaml.safe_dump(r.json(), default_flow_style=False)
