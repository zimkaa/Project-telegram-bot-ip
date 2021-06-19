import sqlite3
import datetime

import pytz


def write_into_db(first_name: str, is_bot: bool, telegram_id: int,
                  date: datetime, message_id: int, text: str,
                  last_name: str = None, username: str = None) -> None:
    """
    Write message in DB
    """
    if sqlite3.connect('.\\IPDB.db'):
        pass
    else:
        print("False")
    with sqlite3.connect('.\\IPDB.db') as db:
        sql = db.cursor()

        sql.execute("""CREATE TABLE IF NOT EXISTS users (
            first_name TEXT NOT NULL,
            is_bot BOOL NOT NULL,
            telegram_id INTEGER NOT NULL UNIQUE,
            last_name TEXT,
            username TEXT)""")

        sql.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            text_message TEXT NOT NULL,
            telegram_id INTEGER NOT NULL,
            datetime NUMERIC NOT NULL)""")

        timezone = pytz.timezone("Europe/Moscow")
        date_message = date.astimezone(timezone)

        data = telegram_id
        sql.execute(
            f"SELECT telegram_id FROM users WHERE telegram_id == {data}")

        if sql.fetchone() is None:
            sql.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                (first_name, is_bot, telegram_id, last_name, username))

        sql.execute(
            "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
            (message_id, text, telegram_id, date_message))
