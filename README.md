# WhatsSheet

A WhatsApp webhook service that processes messages and formats them for spreadsheet entry.

## Project Structure

```
WhatsSheet/
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── controllers/
│   │   └── whatsapp_controller.py
│   ├── models/
│   │   └── expense.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── whatsapp_routes.py
│   ├── services/
│   │   └── price_processor/
│   │       ├── __init__.py
│   │       └── processor.py
│   └── views/
│       └── whatsapp_view.py
├── app.py
├── requirements.txt
└── README.md
```

## Architecture

The project follows the MVC (Model-View-Controller) pattern with additional layers:

- **Models**: Data structures and business logic
- **Views**: Response formatting and presentation
- **Controllers**: Request handling and coordination
- **Routes**: URL endpoints and request routing
- **Services**: Core business logic and processing
- **Config**: Application configuration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Flask application:
```bash
python app.py
```

### Message Format

Send messages in the following format:
- Basic: `19,20 café lifestyle`
- With split: `19,20 café lifestyle (dividir)`

The message will be processed and return a confirmation with the date, price, product, and category. 