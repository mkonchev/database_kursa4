if __name__ == "__main__":
    from Connection.DBConnection import DatabaseConnection

    db = DatabaseConnection("Connection/db_config.ini")
    db.connect()
    # try:
    #     groups = Groups(db.connection)
    #     # Добавление группы
    #     groups.add_group("Group 1")
    #     # Получение всех групп
    #     print(groups.get_all_groups())
    #     # Удаление группы
    #     groups.delete_group(1)
    # finally:
    db.close()
