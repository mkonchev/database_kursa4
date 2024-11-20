class Marks:
    def __init__(self, connection):
        self.connection = connection

    def get_all_marks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM marks")
            return cursor.fetchall()

