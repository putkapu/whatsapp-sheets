from flask import Response, current_app, redirect
from src.services.user_service import UserService
import logging

class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.logger = logging.getLogger(__name__)
    def signup(self, name: str, phone_number: str, password: str, google_sheets_id: str) -> Response:
        is_success, message, id = self.user_service.signup(name, phone_number, password, google_sheets_id)
        if is_success:
            client_id = current_app.config["GOOGLE_CLIENT_ID"]
            redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
            scope = "https://www.googleapis.com/auth/spreadsheets"
            state = f'user_id:{id}'
            oauth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}"
                f"&redirect_uri={redirect_uri}"
                f"&response_type=code"
                f"&scope={scope}"
                f"&access_type=offline"
                f"&prompt=consent"
                f"&state={state}"
            )
            return redirect(oauth_url, code=302)
        else:
            return Response(message, status=400, mimetype="text/plain") 