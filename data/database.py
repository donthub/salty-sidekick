import logging
import os
import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, sql_path='database.sql', db_path='database.db'):
        self.sql_path = sql_path
        self.db_path = db_path
        self.connection = None
        self.cursor = None

        self.is_sql_setup = os.path.exists(self.sql_path) and not os.path.exists(self.db_path)
        self.connect()
        self.setup_tables()

    def add_log(self, log):
        self.insert_log(log.p1_name, log.p1_amount, log.p1_streak, log.p2_name, log.p2_amount, log.p2_streak, log.tier,
                        log.winner, log.mode)

    def insert_log(self, p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode):
        self.cursor.execute("""
            INSERT INTO logs (p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode, datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'));
        """, [p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode])
        self.connection.commit()

    def get_logs(self):
        self.cursor.execute("""
            SELECT p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode, datetime FROM logs ORDER BY id ASC;
        """)
        return self.cursor.fetchall()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except Error as e:
            logging.error(e)

    def setup_tables(self):
        if self.is_sql_setup:
            with open(self.sql_path, 'r', encoding='utf-8') as file:
                self.cursor.executescript(file.read())
        else:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    p1_name TEXT,
                    p1_amount INTEGER,
                    p1_streak INTEGER,
                    p2_name TEXT,
                    p2_amount INTEGER,
                    p2_streak INTEGER,
                    tier TEXT,
                    winner TEXT,
                    mode TEXT,
                    datetime TEXT
                );
            """)
            self.connection.commit()
