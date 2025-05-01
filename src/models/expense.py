from dataclasses import dataclass
from datetime import datetime

@dataclass
class Expense:
    price: float
    product: str
    category: str
    date: str
    is_split: bool = False

    @classmethod
    def from_processor_data(cls, data: dict) -> 'Expense':
        """Create an Expense instance from processed data."""
        return cls(
            price=float(data['price']),
            product=data['product'],
            category=data['category'],
            date=data['date'],
            is_split=data.get('is_split', False)
        ) 