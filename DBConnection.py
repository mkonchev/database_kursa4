import psycopg2


class DatabaseConnection:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to PostgreSQL database.")
        except UnicodeDecodeError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
