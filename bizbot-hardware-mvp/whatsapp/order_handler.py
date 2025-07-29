from mysql.db import fetch_products, insert_order
from typing import Optional
import re

def handle_command(message: str, user_id: str) -> str:
    """
    Process user commands and return appropriate responses.
    
    Args:
        message: User's message text
        user_id: Unique identifier for the user
        
    Returns:
        Formatted response string
    """
    try:
        message = message.lower().strip()
        
        # Price Inquiry
        if any(word in message for word in ["price", "cost", "how much"]):
            return _handle_price_request(message)
            
        # Order Processing
        elif any(word in message for word in ["order", "buy", "purchase"]):
            return _handle_order_request(message, user_id)
            
        # Payment Info
        elif any(word in message for word in ["pay", "payment", "mpesa"]):
            return _handle_payment_request()
            
        # Order Tracking
        elif any(word in message for word in ["track", "status", "delivery"]):
            return _handle_tracking_request(user_id)
            
        # Default Help
        else:
            return _get_help_message()
            
    except Exception as e:
        return f"⚠️ Sorry, I encountered an error: {str(e)}"

def _handle_price_request(message: str) -> str:
    """Handle product price inquiries"""
    products = fetch_products()
    
    # Check if asking about specific product
    for product in products:
        if product['name'].lower() in message:
            return f"💰 {product['name']}: KES {product['price']} per {product['unit']}"
    
    # Show all products if no specific request
    response = ["📋 Current Prices:"]
    for product in products[:5]:  # Show top 5 to avoid long messages
        response.append(f"- {product['name']}: KES {product['price']}/{product['unit']}")
    response.append("\nReply with 'price [item]' for details")
    return "\n".join(response)

def _handle_order_request(message: str, user_id: str) -> str:
    """Process order commands"""
    # Extract quantity
    quantity_match = re.search(r'\d+', message)
    if not quantity_match:
        return "❌ Please specify quantity (e.g. 'order 2 bags of cement')"
    quantity = int(quantity_match.group())
    
    # Find product
    products = fetch_products()
    product = None
    for p in products:
        if p['name'].lower() in message:
            product = p
            break
    
    if not product:
        return "❌ Product not found. Try 'price' to see available items"
    
    # Place order
    try:
        order_id = insert_order(
            customer_id=user_id,
            product_id=product['id'],
            quantity=quantity
        )
        total = quantity * product['price']
        return (
            f"✅ Order #{order_id} confirmed!\n"
            f"• Item: {product['name']}\n"
            f"• Qty: {quantity} {product['unit']}\n"
            f"• Total: KES {total}\n"
            f"Reply 'payment' for payment options"
        )
    except Exception as e:
        return f"❌ Failed to place order: {str(e)}"

def _handle_payment_request() -> str:
    """Return payment information"""
    return (
        "💳 Payment Options:\n"
        "1. M-Pesa Paybill: 123456\n"
        "   Account: Your phone number\n"
        "2. Cash on Delivery\n"
        "3. Bank Transfer:\n"
        "   Bank: Equity\n"
        "   Acc: BizBot X\n"
        "   Code: 123456"
    )

def _handle_tracking_request(user_id: str) -> str:
    """Handle order tracking"""
    # In a real implementation, you would query the database here
    return (
        f"📦 Order Status for #{user_id}:\n"
        "• 2 bags Cement: Being prepared\n"
        "• Estimated delivery: Tomorrow\n"
        "• Delivery rider: James (0722...)"
    )

def _get_help_message() -> str:
    """Default help message"""
    return (
        "🛠️ *BizBot X Help*\n"
        "I can help with:\n"
        "• *Price* - Check product prices\n"
        "• *Order* - Place new orders\n"
        "• *Payment* - Payment options\n"
        "• *Track* - Check order status\n\n"
        "Try: 'price of nails' or 'order 3 bags cement'"
    )