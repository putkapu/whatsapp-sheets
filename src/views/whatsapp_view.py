from typing import Tuple
from src.models.expense import Expense

class WhatsAppView:
    @staticmethod
    def format_invalid_format() -> str:
        return (
            "Formato inválido. Envie algo como:\n"
            "`19,20 café lifestyle`\n"
            "ou\n"
            "`19,20 café lifestyle (dividir)`"
        )

    @staticmethod
    def format_sheets_save_error() -> str:
        return "Erro ao salvar no Google Sheets. Por favor, tente novamente."

    @staticmethod
    def format_sheets_connection_error() -> str:
        return "Erro ao conectar com o Google Sheets. Por favor, verifique suas credenciais."

    @staticmethod
    def format_success(expense: Expense) -> str:
        return (
            f"Gravado ✔️\n"
            f"Data: {expense.date}\n"
            f"Preço: {expense.price}\n"
            f"Produto: {expense.product}\n"
            f"Categoria: {expense.category}"
        )

    @staticmethod
    def format_twiml_response(message: str) -> Tuple[str, str]:
        """Format the response as TwiML."""
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""
        return twiml, 'application/xml' 