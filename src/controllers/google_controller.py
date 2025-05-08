import logging

# from src.services.google_service import GoogleService
from flask import current_app, Response, request
import json


class GoogleController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.google_service = GoogleService()

    def handle_oauth2callback(self) -> Response:
        """Handle Google OAuth2 callback."""
        try:

            current_app.logger.info("Received Google OAuth2 callback")
            code = request.args.to_dict().get("code")

            import requests

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
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )

            # response = response.json()

            current_app.logger.info(f"Google OAuth2 callback response: {response}")
            # response = self.google_service.handle_oauth2callback(request_data)
            current_app.logger.info("Successfully processed Google OAuth2 callback")
            return response

        except Exception as e:
            current_app.logger.error(
                f"Error processing Google OAuth2 callback: {str(e)}"
            )
            return Response(status=500)
