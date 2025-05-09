from dotenv import load_dotenv
from flask import Flask, jsonify
from src.config.settings import Config
from src.routes import whatsapp_bp, google_bp, user_bp
import logging
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(level=app.config["LOG_LEVEL"], format=app.config["LOG_FORMAT"])

    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(google_bp)
    app.register_blueprint(user_bp)

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok"}), 200

    return app

app = create_app()
if __name__ == "__main__":
    app.run()
