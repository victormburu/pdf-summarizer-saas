def create_payment_link(email, plan):
    # You can later dynamically create Paystack links here
    if "Daily" in plan:
        return "https://paystack.com/pay/daily-plan-link"
    elif "Weekly" in plan:
        return "https://paystack.com/pay/weekly-plan-link"
    elif "Monthly" in plan:
        return "https://paystack.com/pay/monthly-plan-link"
    return "https://paystack.com/pay/default"

# MOCK PAYMENT CHECK (replace later with real API call)
def check_payment_status(email):
    # In real case, query your backend or Paystack API to verify by email or ref
    # For testing, simulate successful payment
    return True  # 🔁 Replace this with actual payment API check
