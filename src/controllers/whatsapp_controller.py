from flask import request, Response
from src.services.user_service import UserService
from src.services.expense_service import ExpenseService
from src.views.whatsapp_view import WhatsAppView
import logging


class WhatsAppController:
    def __init__(self):
        self.view = WhatsAppView()
        self.user_service = UserService()
        self.expense_service = ExpenseService()
        self.logger = logging.getLogger(__name__)

    def handle_webhook(self) -> Response:
        """Handle incoming WhatsApp webhook requests."""
        incoming = request.values.get("Body", "").strip()
        cellphone_number = request.values.get("From", "").strip().split(":")[-1]

        is_valid, error_message, user = self.user_service.validate_user(
            cellphone_number
        )
        if not is_valid:
            twiml, mimetype = self.view.format_twiml_response(error_message)
            return Response(twiml, mimetype=mimetype)

        is_success, message, expense = self.expense_service.process_expense(
            incoming, user
        )
        if is_success:
            message = self.view.format_success(expense)

        twiml, mimetype = self.view.format_twiml_response(message)
        return Response(twiml, mimetype=mimetype)
