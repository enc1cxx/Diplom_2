import requests
import allure
from constants.assertions_code import AssertCode
from constants.assertions_messages import AssertMessages
from constants.assertions_success import AssertSuccess
from constants.messages import Messages
from constants.urls import Url
from helpers.helpers import create_order


@allure.epic("Stellar Burger")
@allure.feature("Создание заказа")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Алексей Александров")
class TestCreateOrder:

    @allure.title("Проверка создания заказа без ингредиентов и без авторизации")
    @allure.description(f"{AssertCode.STATUS_400}{AssertMessages.INGREDIENTS_ID_MUST_BE_PROVIDES}")
    def test_create_empty_order_unauthorized(self):
        payload = {"ingredients": []}
        with allure.step("Пробуем создать заказ без ингредиентов и без авторизации"):
            response = requests.post(Url.CREATE_ORDER, data=payload)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_400}{AssertMessages.INGREDIENTS_ID_MUST_BE_PROVIDES}"):
            assert response.status_code == 400 and response_json["message"] == Messages.INGREDIENTS_ID_MUST_BE_PROVIDES

    @allure.title("Проверка создания заказа c ингредиентами и без авторизации")
    @allure.description(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}")
    def test_create_order_unauthorized(self):
        ingredients = create_order()
        payload = {"ingredients": ingredients}
        with allure.step("Пробуем создать заказ с корректными ингредиентами и без авторизации"):
            response = requests.post(Url.CREATE_ORDER, data=payload)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}"):
            assert response.status_code == 200 and response_json["success"] is True

    @allure.title("Проверка создания заказа с некорректным хэшем ингредиентов и без авторизации")
    @allure.description(AssertCode.STATUS_500)
    def test_create_incorrect_order_unauthorized(self):
        payload = {"ingredients": ['123', '123', '123']}
        with allure.step("Пробуем создать заказ с некорректными ингредиентами и без авторизации"):
            response = requests.post(Url.CREATE_ORDER, data=payload)
        with allure.step(AssertCode.STATUS_500):
            assert response.status_code == 500

    @allure.title("Проверка создания заказа без ингредиентов и с авторизацией")
    @allure.description(f"{AssertCode.STATUS_400}{AssertMessages.INGREDIENTS_ID_MUST_BE_PROVIDES}")
    def test_create_empty_order_authorized(self, user_returns_token):
        headers = {'Authorization': user_returns_token}
        payload = {"ingredients": []}
        with allure.step("Пробуем создать заказ без ингредиентов и с авторизацией"):
            response = requests.post(Url.CREATE_ORDER, data=payload, headers=headers)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_400}{AssertMessages.INGREDIENTS_ID_MUST_BE_PROVIDES}"):
            assert response.status_code == 400 and response_json["message"] == Messages.INGREDIENTS_ID_MUST_BE_PROVIDES

    @allure.title("Проверка создания заказа c ингредиентами и с авторизацией")
    @allure.description(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}")
    def test_create_order_authorized(self, user_returns_token):
        headers = {'Authorization': user_returns_token}
        ingredients = create_order()
        payload = {"ingredients": ingredients}
        with allure.step("Пробуем создать заказ с корректными ингредиентами и с авторизацией"):
            response = requests.post(Url.CREATE_ORDER, data=payload, headers=headers)
        response_json = response.json()
        with allure.step(f"{AssertCode.STATUS_200}{AssertSuccess.TRUE}"):
            assert response.status_code == 200 and response_json["success"] is True

    @allure.title("Проверка создания заказа с некорректным хэшем ингредиентов и с авторизацией")
    @allure.description(AssertCode.STATUS_500)
    def test_create_incorrect_order_authorized(self, user_returns_token):
        headers = {'Authorization': user_returns_token}
        payload = {"ingredients": ['123', '123', '123']}
        with allure.step("Пробуем создать заказ с некорректными ингредиентами и с авторизацией"):
            response = requests.post(Url.CREATE_ORDER, data=payload, headers=headers)
        with allure.step(AssertCode.STATUS_500):
            assert response.status_code == 500
