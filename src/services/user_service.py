from src.config.database import SessionLocal
from src.models.user import User
from typing import Tuple, Optional
import logging
from werkzeug.security import generate_password_hash
from psycopg2 import OperationalError
from sqlalchemy.exc import (
    DatabaseError, 
    InterfaceError, 
    InternalError, 
    ProgrammingError,
    DisconnectionError,
    InvalidatePoolError,
    TimeoutError
)
import time
import random

MAX_RETRIES = 5

class UserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _get_db(self):
        return SessionLocal()

    def _execute_with_retry(self, operation, operation_name: str):
        """
        Execute database operation with retry logic for connection issues.
        Uses exponential backoff with jitter to handle cold database starts.
        """
        for attempt in range(MAX_RETRIES):
            try:
                return operation()
            except (OperationalError, DisconnectionError, InvalidatePoolError, TimeoutError, InterfaceError) as e:
                self.logger.warning(f"Database connection error in {operation_name} (attempt {attempt+1}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    # Exponential backoff with jitter: 1s, 2-4s, 4-8s, 8-16s
                    base_delay = 2 ** attempt
                    jitter = random.uniform(0.5, 1.5)
                    delay = base_delay * jitter
                    self.logger.info(f"Retrying {operation_name} in {delay:.1f} seconds...")
                    time.sleep(delay)
                    continue
                self.logger.error(f"Max retries reached for {operation_name}")
                raise
            except (DatabaseError, InternalError, ProgrammingError) as e:
                self.logger.error(f"Database error in {operation_name}: {str(e)}")
                raise
            except Exception as e:
                self.logger.error(f"Unexpected error in {operation_name}: {str(e)}")
                raise

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
        def _validate_operation():
            with self._get_db() as db:
                user = db.query(User).filter(User.phone_number == phone_number).first()
                if not user:
                    self.logger.warning(
                        f"Unauthorized access attempt from phone number: {phone_number}"
                    )
                    return False, "Acesso não autorizado.", None

                if not user.is_active:
                    self.logger.warning(
                        f"Inactive user attempt from phone number: {phone_number}"
                    )
                    return False, "Sua conta está inativa.", None

                if not user.google_sheets_id or not user.google_token:
                    self.logger.warning(
                        f"Incomplete Google Sheets configuration for user: {phone_number}"
                    )
                    return (
                        False,
                        "Configuração do Google Sheets incompleta. Por favor, configure suas credenciais.",
                        None,
                    )

                return True, "", user

        try:
            return self._execute_with_retry(_validate_operation, "validate_user")
        except (OperationalError, DisconnectionError, InvalidatePoolError, TimeoutError, InterfaceError):
            return False, "Erro de conexão com o banco de dados. Tente novamente.", None
        except (DatabaseError, InternalError, ProgrammingError):
            return False, "Erro ao validar usuário.", None
        except Exception:
            return False, "Erro ao validar usuário.", None

    def signup(self, name: str, phone_number: str, password: str, google_sheets_id: str) -> Tuple[bool, str, Optional[User]]:
        def _signup_operation():
            with self._get_db() as db:
                existing_user = db.query(User).filter(User.phone_number == phone_number).first()
                if existing_user:
                    return False, "Usuário já existe.", None
                user = User(
                    name=name,
                    phone_number=phone_number,
                    password=generate_password_hash(password),
                    google_sheets_id=google_sheets_id
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                return True, "Usuário criado com sucesso.", user

        try:
            return self._execute_with_retry(_signup_operation, "signup")
        except (OperationalError, DisconnectionError, InvalidatePoolError, TimeoutError, InterfaceError):
            return False, "Erro de conexão com o banco de dados. Tente novamente.", None
        except (DatabaseError, InternalError, ProgrammingError):
            return False, "Erro ao criar usuário.", None
        except Exception:
            return False, "Erro ao criar usuário.", None

    def update_google_token(self, user_id: int, google_token: str) -> Tuple[bool, str, Optional[User]]:
        def _update_token_operation():
            with self._get_db() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    return False, "Usuário não encontrado.", None
                user.google_token = google_token
                db.commit()
                db.refresh(user)
                return True, "Token do Google Sheets atualizado com sucesso.", user

        try:
            return self._execute_with_retry(_update_token_operation, "update_google_token")
        except (OperationalError, DisconnectionError, InvalidatePoolError, TimeoutError, InterfaceError):
            return False, "Erro de conexão com o banco de dados. Tente novamente.", None
        except (DatabaseError, InternalError, ProgrammingError):
            return False, "Erro ao atualizar token do Google Sheets.", None
        except Exception:
            return False, "Erro ao atualizar token do Google Sheets.", None
