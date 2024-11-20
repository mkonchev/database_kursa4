import psycopg2
import configparser


class DatabaseConnection:
    def __init__(self, config_path="Connection/db_config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        db_type = self.config["database"]["type"]
        if db_type not in ["sqlite", "postgresql", "mysql"]:
            raise ValueError(f"Unsupported database type: {db_type}")

        self.db_type = db_type
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.config["database"]["host"],
                port=self.config["database"]["port"],
                user=self.config["database"]["user"],
                password=self.config["database"]["password"],
                database=self.config["database"]["database"]
            )
            print("Connected to PostgreSQL database.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
