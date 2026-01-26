import urllib.request, json, traceback
def ask(text):
    try:
        data = json.dumps({"messages":[{"role":"user","content":text}],"max_tokens":50}).encode()
        req = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions",
                                     data=data,
                                     headers={"Content-Type":"application/json"})
        raw = urllib.request.urlopen(req).read()
        reply = json.loads(raw)["choices"][0]["message"]["content"].strip()
        print("SERVER SAID:", repr(reply))   # always show what we got
        return reply if reply else "I heard you but the reply was empty."
    except Exception as e:
        print("TINY-BRAIN ERROR:", e)
        traceback.print_exc()
        return "Sorry, I could not reach my brain."