import sqlite3
import os

def connection():
    try:
        path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'example_server.db'
        )
        sqlite_connection = sqlite3.connect(path)

    except Exception as e:
        print({e})
        exit()
    else:
        return sqlite_connection

if __name__ == "__main__":
    connection()