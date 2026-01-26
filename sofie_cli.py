# sofie_cli.py

from core_sofie import get_sofie_reply

print("SOFIE is ready. Type your message or 'exit' to quit.")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye.")
        break

    reply = get_sofie_reply(user_input)
    print("S.O.F.I.E.:", reply)
