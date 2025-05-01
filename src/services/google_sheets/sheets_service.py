from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

class GoogleSheetsService:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Initialize the Google Sheets service.
        
        Args:
            credentials_path: Path to the service account credentials JSON file
            spreadsheet_id: ID of the Google Spreadsheet to use
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()
        self.logger = logging.getLogger(__name__)

    def append_expense(self, expense_data: Dict[str, Any]) -> bool:
        """
        Append an expense to the spreadsheet.
        
        Args:
            expense_data: Dictionary containing expense data
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
            # Format the row data
            row = [
                expense_data['date'],
                str(expense_data['price']),
                expense_data['product'],
                expense_data['category'],
                'Sim' if expense_data.get('is_split', False) else 'Não'
            ]

            # Prepare the request
            body = {
                'values': [row]
            }

            # Append the row
            result = self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Expenses!A:E',  # Assuming we have a sheet named 'Expenses'
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            self.logger.info(f"Successfully appended expense: {expense_data}")
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