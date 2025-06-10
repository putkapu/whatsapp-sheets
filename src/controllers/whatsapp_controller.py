from flask import request, Response, current_app
from src.services.user_service import UserService
from src.services.expense_service import ExpenseService
from src.views.whatsapp_view import WhatsAppView

class WhatsAppController:
    def __init__(self):
        self.view = WhatsAppView()
        self.user_service = UserService()
        self.expense_service = ExpenseService()

    def handle_webhook(self) -> Response:
        """Handle incoming WhatsApp webhook requests."""
        incoming = request.values.get("Body", "").strip()
        cellphone_number = request.values.get("From", "").strip().split(":")[-1]

        current_app.logger.info(f"Received webhook request from {cellphone_number}")
        current_app.logger.debug(f"Message content: {incoming}")

        is_valid, error_message, user = self.user_service.validate_user(cellphone_number)
        if not is_valid:
            current_app.logger.warning(f"Invalid user attempt from {cellphone_number}: {error_message}")
            twiml, mimetype = self.view.format_twiml_response(error_message)
            return Response(twiml, mimetype=mimetype)

        current_app.logger.debug(f"User validated successfully: {user}")

        is_success, message, expense = self.expense_service.process_expense(
            incoming, user
        )
        if is_success:
            current_app.logger.info(f"Expense processed successfully for user {user}: {expense}")
            message = self.view.format_success(expense)
        else:
            current_app.logger.warning(f"Failed to process expense for user {user}: {message}")

        twiml, mimetype = self.view.format_twiml_response(message)
        current_app.logger.debug(f"Sending response: {message}")
        return Response(twiml, mimetype=mimetype)
