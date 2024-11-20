import configparser
import bcrypt


class Authenticator:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def verify_user(self, username, password):
        # Проверяем наличие пользователя в конфиге
        if username in self.config["users"]:
            stored_hash = self.config["users"][username]
            role = self.config["roles"].get(username, "user")  # Роль по умолчанию — пользователь

            # Проверяем пароль
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return True, role
            else:
                return False, None  # Неверный пароль
        else:
            return False, None  # Пользователь не найден
