import copy
import pytest
from constants.assertions_code import AssertCode
from constants.assertions_messages import AssertMessages
from constants.assertions_success import AssertSuccess
from constants.messages import Messages
from helpers.helpers import *
from test_data.update_user_data import TestData


@allure.epic("Stellar Burger")
@allure.feature("Изменение данных пользователя")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Алексей Александров")
class TestUpdateUser:

    @allure.title("Проверка изменения данных пользователя без авторизации")
    @allure.description(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.SHOULD_BE_AUTHORIZED}")
    @pytest.mark.parametrize('parameter', TestData.UPDATE_DATA)
    def test_update_user_without_authorization(self, user_returns_data, parameter):
        payload_copy = copy.copy(user_returns_data)
        payload_copy[parameter] = "something"
        with allure.step("Пробуем изменить данные пользователя без авторизации"):
            response = requests.patch(Url.UPDATE_USER, data=payload_copy)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.SHOULD_BE_AUTHORIZED}"):
            assert response.status_code == 401 and response_json["success"] is False and \
                   response_json["message"] == Messages.SHOULD_BE_AUTHORIZED

    @allure.title("Проверка изменения данных пользователя с авторизацией")
    @allure.description(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}")
    @pytest.mark.parametrize('parameter', TestData.UPDATE_DATA)
    def test_update_user_with_authorization(self, parameter):
        user_data = create_user()
        token = user_login(user_data)
        headers = {'Authorization': token}
        updated_user_data = user_data[parameter] = "something"
        with allure.step("Пробуем изменить данные пользователя с авторизацией"):
            response = requests.patch(Url.UPDATE_USER, data=updated_user_data, headers=headers)
        response_json = response.json()
        delete_user(token)
        with allure.step(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}"):
            assert response.status_code == 200 and response_json["success"] is True
