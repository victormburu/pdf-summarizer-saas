from typing import Dict, List, Optional
from dataclasses import dataclass
import random

@dataclass
class ResponseTemplate:
    """Structure for holding response templates with variations"""
    key: str
    templates: List[str]
    emoji: str = ""
    quick_replies: Optional[List[str]] = None

# Response template collection
RESPONSES = {
    "greeting": ResponseTemplate(
        key="greeting",
        emoji="👋",
        templates=[
            "Hello from BizBot X! How can I help?",
            "Welcome to BizBot X! What do you need today?",
            "Hi there! Ready to assist with your hardware needs."
        ],
        quick_replies=["Prices", "Order", "Track", "Payment"]
    ),
    "price_list": ResponseTemplate(
        key="price_list",
        emoji="💰",
        templates=[
            "Here are our current prices:",
            "Check out our latest prices:",
            "Current product prices:"
        ]
    ),
    "order_help": ResponseTemplate(
        key="order_help",
        emoji="🛒",
        templates=[
            "To order, reply with product name and quantity",
            "Please specify what and how much you want to order",
            "Type the item name and quantity you need"
        ]
    ),
    "payment_info": ResponseTemplate(
        key="payment_info",
        emoji="💳",
        templates=[
            "We accept these payment methods:",
            "Here are our payment options:",
            "You can pay through:"
        ],
        quick_replies=["M-Pesa", "Cash", "Bank Transfer"]
    ),
    "tracking_info": ResponseTemplate(
        key="tracking_info",
        emoji="📦",
        templates=[
            "Your order status:",
            "Here's your order update:",
            "Current delivery status:"
        ]
    ),
    "fallback": ResponseTemplate(
        key="fallback",
        emoji="🤖",
        templates=[
            "I didn't understand that. Try one of these options:",
            "Sorry, can you try one of these commands?",
            "Not sure what you need. Here's what I can do:"
        ]
    )
}

def generate_response(response_key: str, **variables) -> str:
    """
    Generate dynamic responses from templates
    
    Args:
        response_key: Key for response type (greeting, price_list, etc.)
        variables: Dynamic values to insert into template
        
    Returns:
        Formatted response string with emoji and quick replies
    """
    template = RESPONSES.get(response_key, RESPONSES["fallback"])
    chosen_template = random.choice(template.templates)
    
    response = f"{template.emoji} {chosen_template}"
    
    # Insert variables
    if variables:
        response = response.format(**variables)
    
    # Add quick replies if available
    if template.quick_replies:
        reply_options = "\n".join(f"🔹 {reply}" for reply in template.quick_replies)
        response = f"{response}\n\n{reply_options}"
    
    return response

# Example usage
if __name__ == "__main__":
    print(generate_response("greeting"))
    print("\n" + generate_response("price_list"))
    print("\n" + generate_response("payment_info"))