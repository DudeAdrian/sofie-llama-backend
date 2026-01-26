import requests

# Change this if your server is on a different port or host
LLAMA_SERVER_URL = "http://127.0.0.1:8080/completion"

def test_llama_server(prompt="Hello, Sofie!", n_predict=128):
    payload = {
        "prompt": prompt,
        "n_predict": n_predict
    }
    try:
        response = requests.post(LLAMA_SERVER_URL, json=payload)
        response.raise_for_status()
        print("Response from Llama Server:")
        print(response.json())
    except Exception as e:
        print(f"Error communicating with Llama Server: {e}")

if __name__ == "__main__":
    test_llama_server()