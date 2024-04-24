import requests
import json

url = "http://m1.tme-crypto.fr:8888/"

headers = {
    'Content-Type': 'application/json',
}

# Tester avec un argument générique
data = {
    "jsonrpc": "2.0",
    "method": "echo",
    "params": {"message": "Hello World"},
    "id": 1
}

# - echo
# - man
# - server.status
# - server.history
# - world.list

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.text)

