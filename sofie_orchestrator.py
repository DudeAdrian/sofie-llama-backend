import requests
from core_sofie import SofieCore

LLAMA_SERVER_URL = "http://127.0.0.1:8080/completion"

# Initialize SofieCore once
sofie_core = SofieCore()

# Helper to build evidence string for prompt
def build_evidence_string(hits):
    evidence_lines = []
    for h in hits:
        label = h['data'].get('label', h['data'].get('name', ''))
        summary = h['data'].get('purpose', '')
        evidence_lines.append(f"- {label}: {summary}")
    return "\n".join(evidence_lines)

# Main function to handle a user message and return Sofie's response
def sofie_respond(user_message, chat_history=None, top_k=3, n_predict=128):
    if chat_history is None:
        chat_history = []
    # 1. Query evidence
    hits = sofie_core.query(user_message, top_k=top_k)
    evidence = build_evidence_string(hits)
    # 2. Build prompt with system, evidence, and chat history
    system_prompt = (
        "You are Sofie, a friendly, knowledgeable wellness AI guide. "
        "Always greet the user warmly, offer wellness advice, and ask how you can help.\n"
    )
    prompt = system_prompt
    if evidence:
        prompt += f"\nEvidence:\n{evidence}\n"
    # Add chat history
    for turn in chat_history:
        prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"
    prompt += f"User: {user_message}\nSofie:"
    # 3. Call Llama server
    payload = {"prompt": prompt, "n_predict": n_predict}
    try:
        response = requests.post(LLAMA_SERVER_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("content", "[No response from Llama server]")
    except Exception as e:
        return f"[Error communicating with Llama server: {e}]"

# Example usage (for testing)
if __name__ == "__main__":
    chat = []
    print("Sofie (context-aware)>  (type 'exit' to quit)")
    while True:
        user = input("You: ").strip()
        if user in {"exit", "quit"}:
            break
        if not user:
            continue  # Ignore empty input
        chat.append({"role": "user", "content": user})
        reply = sofie_respond(user, chat[:-1])  # Exclude current user message from history in prompt
        print(f"Sofie: {reply}")
        chat.append({"role": "sofie", "content": reply})
