from src.services.price_processor import PriceProcessorService
from src.services.google_sheets.sheets_service import GoogleSheetsService
from src.models.expense import Expense
from src.models.user import User
from src.views.whatsapp_view import WhatsAppView
from typing import Tuple
from flask import current_app


class ExpenseService:

    def process_expense(
        self, message: str, user: User
    ) -> Tuple[bool, str, Expense | None]:
        """
        Process an expense message and save it to Google Sheets.

        Args:
            message: The expense message to process
            user: The user who sent the message

        Returns:
            Tuple containing:
            - bool: Whether the operation was successful
            - str: Success/error message
            - Expense: The processed expense if successful, None otherwise
        """
        current_app.logger.debug(f"Processing expense message: {message}")
        is_valid, _, data = PriceProcessorService.process_message(message)

        if not is_valid:
            current_app.logger.warning(f"Invalid expense format received: {message}")
            return False, WhatsAppView.format_invalid_format(), None

        expense = Expense.from_processor_data(data)
        current_app.logger.debug(f"Expense processed: {expense}")

        try:
            sheets_service = GoogleSheetsService(
                token=user.google_token, spreadsheet_id=user.google_sheets_id
            )
            current_app.logger.debug(f"Attempting to save expense to sheet: {user.google_sheets_id}")
            if sheets_service.append_expense(data):
                current_app.logger.info(f"Successfully saved expense to Google Sheets for user {user}")
                return True, WhatsAppView.format_success(expense), expense
            else:
                current_app.logger.error(f"Failed to save expense to Google Sheets for user {user}")
                return False, WhatsAppView.format_sheets_save_error(), None
        except Exception as e:
            current_app.logger.error(f"Error with Google Sheets service for user {user}: {str(e)}")
            return False, WhatsAppView.format_sheets_connection_error(), None
