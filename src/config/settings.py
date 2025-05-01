import logging
import os

class Config:
    DEBUG = True
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-key-for-testing'
    
    # Google Sheets Configuration
    GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    GOOGLE_SPREADSHEET_ID = os.environ.get('GOOGLE_SPREADSHEET_ID', '') 