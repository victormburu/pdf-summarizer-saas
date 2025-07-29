from flask import request, Response
from twilio.twiml.messaging_response import MessagingResponse
from whatsapp.message_processor import process_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def handle_incoming():
    """Handle incoming WhatsApp messages"""
    #get parameter from webhook
    try:
        sender = request.form.get('From', '')
        message_body = request.form.get('Body', '').strip()
        
        logger.info(f"From {sender}: {message_body}")
            
        Response_text = process_message(sender, message_body)
            
            # Create a Twilio MessagingResponse object
        resp = MessagingResponse()
        resp.message(Response_text)
    
        return Response(str(resp), mimetype='text/xml')
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        resp = MessagingResponse()
        resp.message("An error occurred while processing your message.")
        return Response(str(resp), mimetype='text/xml')
       
