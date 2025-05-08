from flask import Blueprint, request
from src.controllers.user_controller import UserController

user_bp = Blueprint("user", __name__)
user_controller = UserController()

@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    phone_number = data.get("phone_number")
    password = data.get("password")
    google_sheets_id = data.get("google_sheets_id")
    return user_controller.signup(name, phone_number, password, google_sheets_id) 