import sys
from pathlib import Path
import pytest
import requests
from urls import AUTH_URL
sys.path.insert(0, str(Path(__file__).parent))
from api_methods import create_user, get_ingredients

@pytest.fixture
def registered_user():
    """Фикстура для создания пользователя перед тестом и удаления после"""
    user_data = create_user()
    yield user_data
    # Удаляем пользователя после теста
    if user_data and "token" in user_data:
        requests.delete(
            f"{AUTH_URL}",
            headers={"Authorization": user_data["token"]}
        )

@pytest.fixture
def auth_token(registered_user):
    """Фикстура для получения токена авторизации"""
    return registered_user["token"] if registered_user else None