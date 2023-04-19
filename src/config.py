import os

from dotenv import load_dotenv


load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN", "default")

MY_ID = os.getenv("MY_ID", "default")

OTHER_ID = os.getenv("OTHER_ID", "default")

URL = os.getenv("URL", "default")
