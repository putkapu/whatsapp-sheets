from flask import Blueprint, current_app, Response
from src.controllers.google_controller import GoogleController

google_bp = Blueprint('google', __name__)

google_controller = GoogleController()

@google_bp.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    """Handle Google OAuth2 callback."""
    try:
        current_app.logger.info("Received Google OAuth2 callback")
        response = google_controller.handle_oauth2callback()
        current_app.logger.info("Successfully processed Google OAuth2 callback")
        return response
    except Exception as e:
        current_app.logger.error(f"Error processing Google OAuth2 callback: {str(e)}")
        return Response(status=500)