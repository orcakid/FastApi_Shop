from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")