from mysql import connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()
HOST=getenv("DB_HOST")
USER=getenv("DB_USER")
PASSWORD=getenv("DB_PASSWORD")
DATABASE=getenv("DB")
conn = connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
def commit():
    conn.commit()