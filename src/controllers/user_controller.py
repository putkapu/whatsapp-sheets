from flask import Response, current_app, redirect
from src.services.user_service import UserService
import json
from urllib.parse import quote

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def signup(self, name: str, phone_number: str, password: str, google_sheets_id: str) -> Response:
        is_success, message, id = self.user_service.signup(name, phone_number, password, google_sheets_id)
        if is_success:
            # Remove any quotes from config values
            client_id = current_app.config["GOOGLE_CLIENT_ID"]
            redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
            # Quote parameters properly
            redirect_uri = quote(redirect_uri, safe="")
            scope = quote("https://www.googleapis.com/auth/spreadsheets", safe="")
            state = quote(f'user_id:{id}', safe="")
            
            oauth_url = (
                "https://accounts.google.com/o/oauth2/v2/auth"
                f"?client_id={client_id}"
                f"&redirect_uri={redirect_uri}"
                f"&response_type=code"
                f"&scope={scope}"
                f"&access_type=offline"
                f"&prompt=consent"
                f"&state={state}"
            )
            return Response(
                json.dumps({
                    "success": True,
                    "message": message,
                    "oauth_url": oauth_url
                }),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(json.dumps({"success": False, "message": message}), status=400, mimetype="application/json") 