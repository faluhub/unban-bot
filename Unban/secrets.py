import os, dotenv

dotenv.load_dotenv()

class Bot:
    TOKEN         = os.getenv("BOT_TOKEN")
    SECRET        = os.getenv("BOT_SECRET")
    ID            = os.getenv("BOT_ID")

class Database:
    HOST          = os.getenv("DB_HOST")
    PORT          = os.getenv("DB_PORT")
    SCHEMA        = os.getenv("DB_SCHEMA")
    USER          = os.getenv("DB_USER")
    PASSWORD      = os.getenv("DB_PASSWORD")

class Website:
    HOST          = os.getenv("WEB_HOST")
    AUTH_URL      = os.getenv("AUTH_URL")
    AUTH_REDIRECT = os.getenv("AUTH_REDIRECT")
