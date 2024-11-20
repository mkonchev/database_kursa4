if __name__ == "__main__":
    from Connection.DBConnection import DatabaseConnection
    from Tables.groups_table import Groups
    from Tables.marks_table import Marks
    from Tables.people_table import People
    from Tables.subjects_table import Subjects

    db = DatabaseConnection("Connection/db_config.ini")
    db.connect()
    try:
        groups = Groups(db.connection)

        print(groups.get_all_groups())

        print()
    finally:
        db.close()
