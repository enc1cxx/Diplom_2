import requests
import allure
from constants.assertions_code import AssertCode
from constants.assertions_messages import AssertMessages
from constants.assertions_success import AssertSuccess
from constants.messages import Messages
from helpers.generators import generate_user_data
from constants.urls import Url
from helpers.helpers import delete_user, user_login


@allure.epic("Stellar Burger")
@allure.feature("Создание пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Алексей Александров")
class TestCreateUser:

    @allure.title("Проверка создания пользователя без емейла")
    @allure.description(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}")
    def test_create_user_without_login(self):
        user_data = generate_user_data()
        payload = {"email": "", "password": user_data["password"], "name": user_data["name"], }
        with allure.step("Пробуем создать пользователя с пустым емейлом"):
            response = requests.post(Url.CREATE_USER, data=payload)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}"):
            assert response.status_code == 403 and (
                    response_json["message"] == Messages.EMAIL_PASS_NAME_REQUIRED)

    @allure.title("Проверка создания пользователя без пароля")
    @allure.description(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}")
    def test_create_user_without_password(self):
        user_data = generate_user_data()
        payload = {"email": user_data["email"], "password": "", "name": user_data["name"], }
        with allure.step("Пробуем создать пользователя с пустым паролем"):
            response = requests.post(Url.CREATE_USER, data=payload)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}"):
            assert response.status_code == 403 and (
                    response_json["message"] == Messages.EMAIL_PASS_NAME_REQUIRED)

    @allure.title("Проверка создания пользователя без имени")
    @allure.description(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}")
    def test_create_user_without_first_name(self):
        user_data = generate_user_data()
        payload = {"email": user_data["email"], "password": user_data["password"], "name": "", }
        with allure.step("Пробуем создать пользователя с пустым именем"):
            response = requests.post(Url.CREATE_USER, data=payload)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_403}{AssertMessages.EMAIL_PASS_NAME_REQUIRED}"):
            assert response.status_code == 403 and (
                    response_json["message"] == Messages.EMAIL_PASS_NAME_REQUIRED)

    @allure.title("Проверка создания пользователя c корректными данными")
    @allure.description(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}")
    def test_create_user(self):
        payload = generate_user_data()
        with allure.step("Пробуем создать пользователя с полным набором корректных данных"):
            response = requests.post(Url.CREATE_USER, data=payload)
        response_json = response.json()
        token = user_login(payload)
        delete_user(token)
        with allure.step(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}"):
            assert response.status_code == 200 and response_json["success"] is True

    @allure.title("Проверка создания пользователя c существующим набором данных")
    @allure.description(f"{AssertCode.STATUS_403}{AssertMessages.USER_ALREADY_EXISTS}")
    def test_create_user_duplicate_login(self):
        payload = generate_user_data()

        with allure.step("Пробуем создать первого пользователя с полным набором корректных данных"):
            requests.post(Url.CREATE_USER, data=payload)
        with allure.step("Пробуем создать второго пользователя с теми же данными"):
            response = requests.post(Url.CREATE_USER, data=payload)
        response_json = response.json()
        token = user_login(payload)
        delete_user(token)
        with allure.step(f"{AssertCode.STATUS_403}{AssertMessages.USER_ALREADY_EXISTS}"):
            assert (response.status_code == 403 and response_json["message"] == Messages.USER_ALREADY_EXISTS)
