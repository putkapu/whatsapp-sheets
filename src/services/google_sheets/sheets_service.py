from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

from src.config.settings import get_config
Config = get_config()

class GoogleSheetsService:
    def __init__(self, token: str, spreadsheet_id: str):
        """
        Initialize the Google Sheets service.
        
        Args:
            token: Token for authentication
            spreadsheet_id: ID of the Google Spreadsheet to use
        """
        self.logger = logging.getLogger(__name__)
        self.spreadsheet_id = spreadsheet_id
        
        try:
            credentials = Credentials.from_authorized_user_info(
            info={
                "refresh_token": token,
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": Config.GOOGLE_CLIENT_ID, 
                "client_secret": Config.GOOGLE_CLIENT_SECRET
            },
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            self.sheet = self.service.spreadsheets()
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
            raise

    def append_expense(self, data: Dict[str, Any]) -> bool:
        """
        Append an expense to the spreadsheet.
        
        Args:
            data: Dictionary containing expense data
                {
                    'date': str,
                    'price': float,
                    'product': str,
                    'category': str,
                    'is_split': bool
                }
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            values = [[
                data['date'],
                data['price'],
                data['product'],
                data['category']
            ]]
            
            body = {
                'values': values,
                'majorDimension': 'ROWS'
            }
            
            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A:E',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            self.logger.info(f"Successfully appended expense: {data}")
            return True
            
        except HttpError as error:
            self.logger.error(f"Error appending expense: {error}")
            return False

    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """
        Get all expenses from the spreadsheet.
        
        Returns:
            List of dictionaries containing expense data
        """
        try:
            result = self.sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range='Expenses!A2:E'  # Skip header row
            ).execute()

            values = result.get('values', [])
            expenses = []

            for row in values:
                if len(row) >= 5:  # Ensure we have all required fields
                    expense = {
                        'date': row[0],
                        'price': float(row[1]),
                        'product': row[2],
                        'category': row[3],
                        'is_split': row[4].lower() == 'sim'
                    }
                    expenses.append(expense)

            return expenses

        except HttpError as error:
            self.logger.error(f"Error getting expenses: {error}")
            return [] 