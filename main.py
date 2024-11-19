if __name__ == "__main__":
    from DBConnection import DatabaseConnection

    db = DatabaseConnection(host="localhost", port=5432, user="postgres", password="1111", database="laba2")
    db.connect()
    db.close()
