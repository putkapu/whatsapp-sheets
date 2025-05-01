from flask import Blueprint, current_app
from src.controllers.whatsapp_controller import WhatsAppController

whatsapp_bp = Blueprint('whatsapp', __name__)

whatsapp_controller = WhatsAppController()

@whatsapp_bp.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle WhatsApp webhook endpoint."""
    try:
        current_app.logger.info("Received WhatsApp webhook request")
        response = whatsapp_controller.handle_webhook()
        current_app.logger.info("Successfully processed WhatsApp webhook")
        return response
    except Exception as e:
        current_app.logger.error(f"Error processing WhatsApp webhook: {str(e)}")
        raise 