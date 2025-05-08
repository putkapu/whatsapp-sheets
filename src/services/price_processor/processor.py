import re
from datetime import datetime


class PriceProcessorService:
    # regex: price (int/float with comma), product (word‐chunk), category (word‐chunk), optional (dividir)
    PATTERN = re.compile(
        r"^\s*(\d+(?:,\d+)?)\s+(.+?)\s+(\w+)(?:\s+\(dividir\))?\s*$", re.IGNORECASE
    )

    @classmethod
    def process_message(cls, message: str) -> tuple[bool, str, dict]:
        """
        Process the incoming message and extract price, product, and category.

        Args:
            message: The incoming message string

        Returns:
            tuple: (is_valid, reply_message, data)
            - is_valid: bool indicating if the message was valid
            - reply_message: The response message to send back
            - data: Dictionary containing the processed data (price, product, category, date)
        """
        message = message.strip()
        m = cls.PATTERN.match(message)

        if not m:
            return (
                False,
                (
                    "Formato inválido. Envie algo como:\n"
                    "`19,20 café lifestyle`\n"
                    "ou\n"
                    "`19,20 café lifestyle (dividir)`"
                ),
                {},
            )

        price, product, category = m.groups()
        # Convert comma to dot for price
        price = price.replace(",", ".")
        # Check if input ends with (dividir)
        if message.lower().endswith("(dividir)"):
            price = str(float(price) / 2)

        # Get current date in dd/mm/yyyy format
        current_date = datetime.now().strftime("%d/%m/%Y")

        data = {
            "price": price,
            "product": product,
            "category": category,
            "date": current_date,
        }

        reply = (
            f"Gravado ✔️\n"
            f"Data: {current_date}\n"
            f"Preço: {price}\n"
            f"Produto: {product}\n"
            f"Categoria: {category}"
        )

        return True, reply, data
