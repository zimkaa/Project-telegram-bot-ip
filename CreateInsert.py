from datetime import datetime
import sqlite3

import pytz


def create_db():

    with sqlite3.connect('.\\IPDB.db') as db:
        sql = db.cursor()

        sql.execute("DROP TABLE IF EXISTS users")
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            is_bot TEXT NOT NULL,
            telegram_id INTEGER NOT NULL UNIQUE,
            last_name TEXT,
            username TEXT)""")

        sql.execute("DROP TABLE IF EXISTS messages")
        sql.execute("""CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_message TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            datetime NUMERIC NOT NULL)""")

        timezone = pytz.timezone("Europe/Moscow")
        data = datetime.now()
        dt = data.astimezone(timezone)

        sql.execute("""INSERT INTO users (
            first_name, is_bot, telegram_id, last_name, username)
            VALUES ("Anton", "False", "11111", "***", "zimkaa")""")

        sql.execute(f"""INSERT INTO messages (
            text_message, user_id, datetime)
            VALUES ( "tratata", "1", "{dt}")""")

        db.commit()


if __name__ == "__main__":
    create_db()
