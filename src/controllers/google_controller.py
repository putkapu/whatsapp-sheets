# from src.services.google_service import GoogleService
from flask import current_app, Response, request
import json
import requests

from src.services.user_service import UserService

class GoogleController:
    def __init__(self):
        self.user_service = UserService()

    def handle_oauth2callback(self) -> Response:
        """Handle Google OAuth2 callback."""
        try:
            current_app.logger.debug("Starting OAuth2 Callback Processing")
            request_args = request.args.to_dict()
            current_app.logger.debug(f"Callback parameters: {json.dumps(request_args)}")
            
            code = request_args.get("code")
            if not code:
                current_app.logger.error("No authorization code received in callback")
                return Response(status=400)

            current_app.logger.debug("Authorization code received successfully")
            token_url = "https://oauth2.googleapis.com/token"
            
            client_id = current_app.config["GOOGLE_CLIENT_ID"]
            client_secret = current_app.config["GOOGLE_CLIENT_SECRET"]
            redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
            
            current_app.logger.debug(f"Using redirect URI: {redirect_uri}")
            
            request_data = {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }

            current_app.logger.debug(f"Making token request to: {token_url}")
            # Log request data without sensitive info
            safe_log_data = {**request_data, 
                           "client_id": f"{client_id[:8]}...", 
                           "client_secret": "***",
                           "code": f"{code[:8]}..."}
            current_app.logger.debug(f"Token request data: {json.dumps(safe_log_data)}")
            
            response = requests.post(token_url, data=request_data)
            current_app.logger.debug(f"Token response status: {response.status_code}")
            
            if not response.ok:
                current_app.logger.error(f"Token request failed with status {response.status_code}: {response.text}")
                return Response(status=response.status_code)

            token_data = response.json()
            current_app.logger.debug("Token response parsed successfully")
            
            state = request_args.get("state")
            if not state or ":" not in state:
                current_app.logger.error("Invalid state parameter received")
                return Response(status=400)

            user_id = int(state.split(":")[1])
            current_app.logger.debug(f"Extracted user_id from state: {user_id}")

            if "refresh_token" not in token_data:
                current_app.logger.error("No refresh token received in response")
                return Response(status=400)

            self.user_service.update_google_token(user_id, token_data["refresh_token"]) 
            current_app.logger.debug(f"Token updated for user_id: {user_id}")
            current_app.logger.info(f"Successfully updated Google token for user_id: {user_id}")
            
            return Response(
                response=json.dumps(token_data), status=200, mimetype="application/json"
            )
        
        except Exception as e:
            current_app.logger.error(
                f"Error processing Google OAuth2 callback: {str(e)}"
            )
            return Response(status=500)
