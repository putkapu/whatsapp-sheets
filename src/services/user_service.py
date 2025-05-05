from src.config.database import SessionLocal
from src.models.user import User
import logging

class UserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_user(self, phone_number: str) -> tuple[bool, str]:
        """
        Validate if a user exists and is active.
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.phone_number == phone_number).first()
            if not user:
                self.logger.warning(f"Unauthorized access attempt from phone number: {phone_number}")
                return False, "Acesso não autorizado."
            
            if not user.is_active:
                self.logger.warning(f"Inactive user attempt from phone number: {phone_number}")
                return False, "Sua conta está inativa."
            
            return True, ""
        except Exception as e:
            self.logger.error(f"Erro ao validar o usuário: {str(e)}")
            return False, "Ocorreu um erro ao validar sua conta."
        finally:
            db.close() 
