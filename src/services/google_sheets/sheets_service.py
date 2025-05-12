from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app

class GoogleSheetsService:
    HEADER = [["Data", "Descrição", "Categoria", "Valor"]]
    RANGE = "A:E"
    HEADER_RANGE = "A1:E"

    def __init__(self, token: str, spreadsheet_id: str):
        """
        Initialize the Google Sheets service.

        Args:
            token: Token for authentication
            spreadsheet_id: ID of the Google Spreadsheet to use
        """
        self.spreadsheet_id = spreadsheet_id

        try:
            credentials = Credentials.from_authorized_user_info(
                info={
                    "refresh_token": token,
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "client_id": current_app.config['GOOGLE_CLIENT_ID'],
                    "client_secret": current_app.config['GOOGLE_CLIENT_SECRET']
                },
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
            self.service = build("sheets", "v4", credentials=credentials)
            self.sheet = self.service.spreadsheets()
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
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
            if not self.header_exists():
                self.write_header()
                self.set_date_format()

            values = [[data["date"], data["product"], data["category"], data["price"]]]

            body = {"values": values, "majorDimension": "ROWS"}

            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=self.RANGE,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body,
            ).execute()

            current_app.logger.info(f"Successfully appended expense: {data}")
            return True

        except HttpError as error:
            current_app.logger.error(f"Error appending expense: {error}")
            return False

    def header_exists(self) -> bool:
        existing_values = (
            self.sheet.values()
            .get(spreadsheetId=self.spreadsheet_id, range=self.HEADER_RANGE)
            .execute()
            .get("values", [])
        )
        return bool(existing_values)

    def write_header(self) -> None:
        self.sheet.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.HEADER_RANGE,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": self.HEADER},
        ).execute()

    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """
        Get all expenses from the spreadsheet.

        Returns:
            List of dictionaries containing expense data
        """
        try:
            result = (
                self.sheet.values()
                .get(spreadsheetId=self.spreadsheet_id, range="A2:E")
                .execute()
            )

            values = result.get("values", [])
            expenses = []

            for row in values:
                if len(row) >= 5:
                    expense = {
                        "Date": row[0],
                        "Product": row[2],
                        "Category": row[3],
                        "Price": float(row[1]),
                    }
                    expenses.append(expense)

            return expenses

        except HttpError as error:
            current_app.logger.error(f"Error getting expenses: {error}")
            return []

    def set_date_format(self):
        requests = [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,  # Change if not the first/default sheet
                        "startColumnIndex": 0,
                        "endColumnIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "DATE",
                                "pattern": "yyyy-mm-dd"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            }
        ]
        body = {"requests": requests}
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()
