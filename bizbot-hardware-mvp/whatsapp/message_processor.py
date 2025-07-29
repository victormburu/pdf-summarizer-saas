import logging
from typing import Dict, Optional
from whatsapp.order_handler import handle_command

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_message(data: Dict) -> Dict:
    """
    Process incoming messages and route to appropriate handler.
    
    Args:
        data: Dictionary containing message data with keys:
              - message: str - The user's message text
              - user_id: str - Unique identifier for the user
              - platform: Optional[str] - Source platform (whatsapp/telegram/etc)
    
    Returns:
        Dict: Response containing:
              - text: str - Response message
              - status: str - success/error
              - metadata: Optional[Dict] - Additional data
    """
    try:
        # Validate input
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
            
        user_message = data.get("message", "").strip().lower()
        user_id = data.get("user_id", "unknown")
        platform = data.get("platform", "unknown")
        
        if not user_message:
            logger.warning(f"Empty message from user {user_id}")
            return {
                "text": "Please send a valid message",
                "status": "error",
                "metadata": {"user_id": user_id}
            }
        
        logger.info(f"Processing message from {user_id}: {user_message[:50]}...")
        
        # Route to command handler
        response = handle_command(
            message=user_message,
            user_id=user_id,
            platform=platform
        )
        
        return {
            "text": response,
            "status": "success",
            "metadata": {
                "user_id": user_id,
                "platform": platform,
                "message_length": len(user_message)
            }
        }
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}", exc_info=True)
        return {
            "text": "Sorry, I encountered an error processing your request",
            "status": "error",
            "metadata": {
                "error": str(e),
                "user_id": data.get("user_id", "unknown")
            }
        }