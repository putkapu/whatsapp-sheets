from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from src.models.user import Base

    Base.metadata.create_all(bind=engine)
