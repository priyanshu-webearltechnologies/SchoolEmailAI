def generate_reply(intent, student_name):
    if intent == "PAYMENT_DONE":
        return f"""
Dear Parent of {student_name},

Thank you for confirming the payment. We acknowledge receipt of the fee.

If you have any further queries, feel free to contact us.

Regards,
School Accounts Office
"""

    elif intent == "EXTENSION_REQUEST":
        return f"""
Dear Parent of {student_name},

We have received your request for an extension. The same has been forwarded to the concerned department for review.

You will be informed shortly regarding approval.

Regards,
School Administration
"""

    elif intent == "FEE_QUERY":
        return f"""
Dear Parent of {student_name},

Thank you for bringing this to our attention. The fee details will be verified by the accounts department.

We will update you at the earliest.

Regards,
School Accounts Office
"""

    elif intent == "RECEIPT_REQUEST":
        return f"""
Dear Parent of {student_name},

Your request for the payment receipt has been noted. The receipt will be shared with you shortly.

Regards,
School Accounts Office
"""

    else:
        return f"""
Dear Parent of {student_name},

Thank you for your message. Our team will review your query and get back to you shortly.

Regards,
School Administration
"""
