class People:
    def __init__(self, connection):
        self.connection = connection

    def get_all_people(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM people")
            return cursor.fetchall()

