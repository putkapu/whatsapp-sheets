from src.services.price_processor import PriceProcessorService
from src.services.google_sheets.sheets_service import GoogleSheetsService
from src.models.expense import Expense
from src.models.user import User
from src.views.whatsapp_view import WhatsAppView
from typing import Tuple
import logging


class ExpenseService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
        is_valid, _, data = PriceProcessorService.process_message(message)

        if not is_valid:
            return False, WhatsAppView.format_invalid_format(), None

        expense = Expense.from_processor_data(data)

        try:
            sheets_service = GoogleSheetsService(
                token=user.google_token, spreadsheet_id=user.google_sheets_id
            )
            if sheets_service.append_expense(data):
                return True, WhatsAppView.format_success(expense), expense
            else:
                return False, WhatsAppView.format_sheets_save_error(), None
        except Exception as e:
            self.logger.error("Error with Google Sheets service: {}", str(e))
            return False, WhatsAppView.format_sheets_connection_error(), None
