from constants.assertions_code import AssertCode
from constants.assertions_messages import AssertMessages
from constants.assertions_success import AssertSuccess
from constants.messages import Messages
from helpers.helpers import *


@allure.epic("Stellar Burger")
@allure.feature("Логин пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Алексей Александров")
class TestLoginUser:

    @allure.title("Проверка логина пользователя c корректными данными")
    @allure.description(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}")
    def test_login_user(self, user_returns_data):
        with allure.step(
                "Пробуем залогиниться пользователем с полным набором корректных данных"
        ):
            response = requests.post(Url.LOGIN, data=user_returns_data)
        response_json = response.json()
        delete_user(response_json.get("accessToken"))
        with allure.step(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}"):
            assert response.status_code == 200 and response_json["success"] is True

    @allure.title("Проверка логина пользователя c корректными данными")
    @allure.description(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.INCORRECT_EMAIL_OR_PASS}")
    def test_login_incorrect_user_data(self):
        user_data = {"email": "email", "password": "password"}
        with allure.step(
                "Пробуем залогиниться пользователем с полным набором корректных данных"
        ):
            response = requests.post(Url.LOGIN, data=user_data)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.INCORRECT_EMAIL_OR_PASS}"):
            assert response.status_code == 401 and response_json["success"] is False and \
                   response_json["message"] == Messages.INCORRECT_EMAIL_OR_PASS
