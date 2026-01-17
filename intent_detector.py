def detect_intent(message):
    message = message.lower()

    if any(word in message for word in ["give me receipt", "please give receipt", "receipt", "bill", "proof", "confirmation", "i have paid give me receipt"]):
        return "RECEIPT_REQUEST"
    
    elif any(word in message for word in ["paid", "payment done", "fees paid", "paid today"]):
        return "PAYMENT_DONE"

    elif any(word in message for word in ["extension", "time", "delay", "late", "soon", "extra days", "more time", "extend", "as soon as possible"]):
        return "EXTENSION_REQUEST"

    elif any(word in message for word in ["wrong", "incorrect", "mistake", "extra"]):
        return "FEE_QUERY"
    
    else:
        return "UNKNOWN"
