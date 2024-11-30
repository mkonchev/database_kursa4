import configparser
import bcrypt
from Connection.DBConnection import DatabaseConnection


class Authenticator:
    def __init__(self, config_path):
        self.db = DatabaseConnection(config_path)

    def verify_user(self, username, password):
        self.db.connect()
        try:
            cursor = self.db.connection.cursor()
            # Проверяем наличие пользователя в таблице `users`
            query = "SELECT id, login, password, role FROM users"
            cursor.execute(query)
            users = cursor.fetchall()

            for user_id, stored_login, stored_password, role in users:
                if bcrypt.checkpw(username.encode('utf-8'), stored_login.encode('utf-8')):
                    # Проверить пароль, если логин совпал
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        return True, role
            return False, None  # Неверный пароль или пользователя нет
        except Exception as e:
            print(f"Error during authentication: {e}")
            return False, None
        finally:
            self.db.close()


# def check_user_exists(user_name: str, password: str) -> bool:
#     with session_factory() as session:
#         users = session.execute(select(Users)).scalars().all()
#         for user in users:
#             if user.check_password(password) and bcrypt.checkpw(user_name.encode('utf-8'),
#                                                                 user.user_name.encode('utf-8')):
#                 return True
#         return False
