from flask import request, Response, current_app
from src.services.price_processor import PriceProcessor
from src.services.google_sheets import GoogleSheetsService
from src.models.expense import Expense
from src.views.whatsapp_view import WhatsAppView

class WhatsAppController:
    def __init__(self):
        self.view = WhatsAppView()
        self.sheets_service = GoogleSheetsService(
            credentials_path=current_app.config['GOOGLE_CREDENTIALS_PATH'],
            spreadsheet_id=current_app.config['GOOGLE_SPREADSHEET_ID']
        )

    def handle_webhook(self) -> Response:
        """Handle incoming WhatsApp webhook requests."""
        incoming = request.values.get('Body', '').strip()
        is_valid, reply, data = PriceProcessor.process_message(incoming)

        if not is_valid:
            message = self.view.format_error()
        else:
            expense = Expense.from_processor_data(data)
            # Save to Google Sheets
            if self.sheets_service.append_expense(data):
                message = self.view.format_success(expense)
            else:
                message = "Erro ao salvar no Google Sheets. Por favor, tente novamente."

        twiml, mimetype = self.view.format_twiml_response(message)
        return Response(twiml, mimetype=mimetype) 