"""Module for manual testing code for 'network' project."""


import requests

url = "http://127.0.0.1:8000/api/token/"

response = requests.post(
    url=url,
    headers={"Content-Type": "application/json"},
    json={"username": "vova", "password": "ahfywepcrbq zpsr11"},
)

print(response.json())
