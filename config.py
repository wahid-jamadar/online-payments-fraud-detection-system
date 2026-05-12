from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost").strip()
    MYSQL_USER = os.getenv("MYSQL_USER", "root").strip()
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "").strip()
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fraud_db").strip()
    
    MODEL_PATH = "model/fraud_model.pkl"
    
    # Flask-Mail configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your_app_password")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "your_email@gmail.com")