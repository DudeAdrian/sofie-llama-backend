import requests

# Example usage for frontend integration
# This function can be called from your React/Next.js app

def send_check_in(message, consent=True, chat_history=None):
    url = "http://localhost:8000/check-in"
    payload = {
        "message": message,
        "consent": consent,
        "chat_history": chat_history or []
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]

if __name__ == "__main__":
    # Example test
    print(send_check_in("How can I rest better?", True))
