from src.config.database import SessionLocal
from src.models.user import User
from typing import Tuple, Optional
import logging


class UserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_user(self, phone_number: str) -> Tuple[bool, str, Optional[User]]:
        """
        Validate if a user exists, is active, and has valid Google Sheets credentials.

        Args:
            phone_number: User's phone number

        Returns:
            Tuple containing:
            - bool: Whether the user is valid
            - str: Error message if invalid, empty string if valid
            - User: User object if valid, None if invalid
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.phone_number == phone_number).first()

            if not user:
                self.logger.warning(
                    "Unauthorized access attempt from phone number: %s", phone_number
                )
                return False, "Acesso não autorizado.", None

            if not user.is_active:
                self.logger.warning(
                    "Inactive user attempt from phone number: %s", phone_number
                )
                return False, "Sua conta está inativa.", None

            if not user.google_sheets_id or not user.google_token:
                self.logger.warning(
                    "Incomplete Google Sheets configuration for user: %s", phone_number
                )
                return (
                    False,
                    "Configuração do Google Sheets incompleta. Por favor, configure suas credenciais.",
                    None,
                )

            return True, "", user
        except Exception as e:
            self.logger.error(f"Error validating user: {str(e)}")
            return False, "Erro ao validar usuário.", None
        finally:
            db.close()
