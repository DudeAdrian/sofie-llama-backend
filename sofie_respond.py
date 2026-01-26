import urllib.request
import json

def ask_sofie():
    prompt = input("Ask S.O.F.I.E.: ")
    data = {
        "stream": False,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        url="http://127.0.0.1:8080/v1/chat/completions",
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
        response = json.loads(raw)
        print("\nS.O.F.I.E. says:\n", response["choices"][0]["message"]["content"])
    except Exception as e:
        print("Error talking to S.O.F.I.E.:", e)
        print("S.O.F.I.E. says:\n I'm here with you.")

if __name__ == "__main__":
    ask_sofie()
