class Groups:
    def __init__(self, connection):
        self.connection = connection

    def get_all_groups(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM groups")
            return cursor.fetchall()

