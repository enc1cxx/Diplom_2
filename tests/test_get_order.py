import allure
import requests

from constants.assertions_code import AssertCode
from constants.assertions_messages import AssertMessages
from constants.assertions_success import AssertSuccess
from constants.messages import Messages
from constants.urls import Url
from helpers.helpers import create_order


@allure.epic("Stellar Burger")
@allure.feature("Получение заказа")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Алексей Александров")
class TestGetOrder:

    @allure.title("Проверка получения заказов неавторизованного пользователя")
    @allure.description(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.SHOULD_BE_AUTHORIZED}")
    def test_get_order_unauthorized(self):
        with allure.step("Пробуем получить заказы без авторизации"):
            response = requests.get(Url.GET_ORDERS)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_401}{AssertSuccess.FALSE}{AssertMessages.SHOULD_BE_AUTHORIZED}"):
            assert response.status_code == 401 and (response_json["message"] == Messages.SHOULD_BE_AUTHORIZED) and (
                    response_json["success"] is False)

    @allure.title("Проверка получения заказов авторизованного пользователя")
    @allure.description(f"{AssertCode.STATUS_200}, количество заказов==1 и {AssertSuccess.TRUE}")
    def test_get_order_authorized(self, user_returns_token):
        headers = {'Authorization': user_returns_token}
        ingredients = create_order()
        payload = {"ingredients": ingredients}
        requests.post(Url.CREATE_ORDER, data=payload, headers=headers)
        with allure.step("Пробуем получить заказы с авторизацией"):
            response = requests.get(Url.GET_ORDERS, headers=headers)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_200}, количество заказов==1 и {AssertSuccess.TRUE}"):
            assert response.status_code == 200 and (response_json["total"] == 1) and (
                    response_json["success"] is True)
