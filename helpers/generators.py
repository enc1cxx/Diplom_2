import random
import string
import allure


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for i in range(length))
    return random_string


def generate_email():
    login = ""

    # для вариативности
    domain = [
        "@mail.ru",
        "@yandex.ru",
        "@rambler.ru",
        "@gmail.com",
    ]

    # для простоты идентификации среди существующих в БД записей
    login += generate_random_string(10) + "_api_autotest_"
    login += random.choice(domain)
    return login


@allure.step("Генерируем пользовательские данные")
def generate_user_data():
    user_data = {}
    login = generate_email()
    password = generate_random_string(10)
    name = generate_random_string(10)

    user_data["email"] = login
    user_data["password"] = password
    user_data["name"] = name
    return user_data