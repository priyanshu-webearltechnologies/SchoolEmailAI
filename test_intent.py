from intent_detector import detect_intent

messages = [
    "I have paid the fees today",
    "Please give me 10 days extension",
    "The fee amount is incorrect",
    "Please send receipt",
    "Hello"
]

for msg in messages:
    print(msg, "→", detect_intent(msg))