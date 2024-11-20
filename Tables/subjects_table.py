class Subjects:
    def __init__(self, connection):
        self.connection = connection

    def get_all_subjects(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM subjects")
            return cursor.fetchall()

