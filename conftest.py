import pytest

from helpers.generators import generate_user_data
from helpers.helpers import *


@allure.step("Создаём пользователя")
@pytest.fixture(scope="function")
def user_returns_data():
    user_data = create_user()
    yield user_data
    token = user_login(user_data)
    delete_user(token)


@allure.step("Создаём пользователя и логинимся")
@pytest.fixture(scope="function")
def user_returns_token():
    user_data = create_user()
    token = user_login(user_data)
    yield token
    delete_user(token)
