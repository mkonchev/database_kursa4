class Groups:
    def __init__(self, connection):
        self.connection = connection

    def add_group(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO groups (name) VALUES (%s)", (name,))
            self.connection.commit()
            print(f"Group '{name}' added successfully.")

    def get_all_groups(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM groups")
            return cursor.fetchall()

    def delete_group(self, group_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM groups WHERE id = %s", (group_id,))
            self.connection.commit()
            print(f"Group with ID {group_id} deleted.")
