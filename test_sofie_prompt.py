import urllib.request
import json

url = "http://127.0.0.1:8080/v1/chat/completions"

payload = {
    "messages": [
        {"role": "system", "content": "You are Sofie, a wise and gentle assistant."},
        {"role": "user", "content": "Hello Sofie, can you hear me?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

response = urllib.request.urlopen(req).read()
print(json.loads(response)["choices"][0]["message"]["content"])
