from mysql.db import fetch_products, insert_order

def process_message(message):
    """Process incoming messages about products and orders"""
    message = message.lower().strip()
    products = fetch_products()  # Cache products to reduce DB calls
    
    # Price inquiry
    if any(word in message for word in ["price", "cost", "how much"]):
        response = ["Available products and prices:"]
        for product in products:
            response.append(f"- {product['name']}: ${product['price']} per {product['unit']}")
        return "\n".join(response)
    
    # Order processing
    if any(word in message for word in ["order", "buy", "purchase"]):
        # Extract quantity (look for numbers in message)
        quantities = [int(s) for s in message.split() if s.isdigit()]
        if not quantities:
            return "Please specify a quantity (e.g., 'order 5 bags of cement')."
        quantity = quantities[0]
        
        # Find product by name (more flexible matching)
        product_name = None
        for product in products:
            if product['name'].lower() in message:
                product_name = product['name']
                product_id = product['id']
                break
        
        if not product_name:
            return "Product not found. Please specify a valid product name."
        
        try:
            # Get customer ID from message or use default
            customer_id = extract_customer_id(message) or 1  # Default to 1 if not found
            
            # Insert order
            order_id = insert_order(
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity
            )
            return (f"✅ Order #{order_id} confirmed: {quantity} {product['unit']} "
                   f"of {product_name} (${quantity * product['price']:.2f})")
        except Exception as e:
            return f"❌ Order failed: {str(e)}"
    
    return ("I can help with product prices or orders. Try:\n"
           "- 'What's the price of nails?'\n"
           "- 'I want to order 5 bags of cement'")

def extract_customer_id(message):
    """Extract customer ID from message if mentioned"""
    # Implement your customer ID extraction logic here
    # Could look for patterns like "for customer 123"
    return None  # Default implementation