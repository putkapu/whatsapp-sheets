from typing import Tuple
from src.models.expense import Expense

class WhatsAppView:
    @staticmethod
    def format_error() -> str:
        return (
            "Formato inválido. Envie algo como:\n"
            "`19,20 café lifestyle`\n"
            "ou\n"
            "`19,20 café lifestyle (dividir)`"
        )

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