import logging
# from src.services.google_service import GoogleService
from flask import current_app, Response, request
import json
import requests

from src.services.user_service import UserService

class GoogleController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_service = UserService()


    def handle_oauth2callback(self) -> Response:
        """Handle Google OAuth2 callback."""
        try:

            current_app.logger.info("Received Google OAuth2 callback")
            code = request.args.to_dict().get("code")

            token_url = "https://oauth2.googleapis.com/token"
            client_id = current_app.config["GOOGLE_CLIENT_ID"]
            client_secret = current_app.config["GOOGLE_CLIENT_SECRET"]
            redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
            request_data = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
            response = requests.post(token_url, data=request_data).json()
            user_id = int(request.args.get("state").split(":")[1])
            self.user_service.update_google_token(user_id, response["access_token"])
            
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        
        except Exception as e:
            current_app.logger.error(
                f"Error processing Google OAuth2 callback: {str(e)}"
            )
            return Response(status=500)
