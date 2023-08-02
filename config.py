import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = "6191542874:AAHhyLFdTIuTanmt-jkINhRrVLiNkaXU8xw"
# TOKEN = os.getenv('BOT_TOKEN')
# host = os.getenv('DB_HOST')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')
# db_name = os.getenv('DB_NAME')
# port = os.getenv('DB_PORT')
PAYMENTS_PROVIDER_TOKEN = os.getenv('PAYMENTS_PROVIDER_TOKEN')

host = "localhost"
user = "root"
password = "bebepassword"
db_name = "mysql"
port = "3306"