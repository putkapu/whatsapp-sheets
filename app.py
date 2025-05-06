from dotenv import load_dotenv
from flask import Flask
from src.config.settings import Config
from src.routes import whatsapp_bp, google_bp
import logging

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT']
    )
    
    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(google_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
