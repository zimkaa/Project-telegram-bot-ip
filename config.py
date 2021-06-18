import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

MY_ID = int(os.getenv('MY_ID'))  # type: ignore

OTHER_ID = int(os.getenv('OTHER_ID'))  # type: ignore

URL = os.getenv('URL')
