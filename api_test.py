import json
import requests
import sys
from pathlib import Path
parameters = {}
parameters["argv"] = sys.argv
try:
    req = requests.post(url="http://127.0.0.1:5001/encode",json=parameters)
except requests.exceptions.ConnectionError:
    print("Server not yet setup or connection refused")
    req = None
if req is not None:
    if req.status_code == 200:
        response = json.loads(req.text)
        print(response)
    else:
        print("Unable to create request. Response code ",req.status_code)

try:
    req = requests.post(url="http://127.0.0.1:5001/decode",json=parameters)
except requests.exceptions.ConnectionError:
    print("Server not yet setup or connection refused")
    req = None
if req is not None:
    if req.status_code == 200:
        response = json.loads(req.text)
        print(response)
    else:
        print("Unable to create request. Response code ",req.status_code)