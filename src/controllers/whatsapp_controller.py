from flask import request, Response, current_app
from src.services.price_processor import PriceProcessorService
# from src.services.google_sheets import GoogleSheetsService
from src.models.expense import Expense
from src.views.whatsapp_view import WhatsAppView
from src.config.database import SessionLocal
from src.models.user import User
from src.services.user_service import UserService
import logging

class WhatsAppController:
    def __init__(self):
        self.view = WhatsAppView()
        # self.sheets_service = GoogleSheetsService(
        #     credentials_path=current_app.config['GOOGLE_CREDENTIALS_PATH'],
        #     spreadsheet_id=current_app.config['GOOGLE_SPREADSHEET_ID']
        # )
        self.user_service = UserService()
        self.logger = logging.getLogger(__name__)

    def handle_webhook(self) -> Response:
        """Handle incoming WhatsApp webhook requests."""
        incoming = request.values.get('Body', '').strip()
        cellphone_number = request.values.get('From', '').strip().split(':')[-1]

        # Validate user
        is_valid, message = self.user_service.validate_user(cellphone_number)
        if not is_valid:
            twiml, mimetype = self.view.format_twiml_response(message)
            return Response(twiml, mimetype=mimetype)

        is_valid, reply, data = PriceProcessorService.process_message(incoming)
        
        if not is_valid:
            message = self.view.format_error()
        else:
            expense = Expense.from_processor_data(data)
            # Save to Google Sheets
            # if self.sheets_service.append_expense(data):
            message = self.view.format_success(expense)
            # else:
            #     message = "Erro ao salvar no Google Sheets. Por favor, tente novamente."

        twiml, mimetype = self.view.format_twiml_response(message)
        return Response(twiml, mimetype=mimetype) 