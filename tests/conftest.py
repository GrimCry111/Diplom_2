import sys
from pathlib import Path
import pytest
import requests

# Добавляем директорию tests в PYTHONPATH
# Это критически важно для корректной работы импортов
sys.path.insert(0, str(Path(__file__).parent))

# Теперь можем импортировать utils без точки
from utils import create_user, BASE_URL

@pytest.fixture
def registered_user():
    """Фикстура для создания пользователя перед тестом и удаления после"""
    user_data = create_user()
    yield user_data
    # Удаляем пользователя после теста
    if user_data and "token" in user_data:
        requests.delete(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": user_data["token"]}
        )

@pytest.fixture
def auth_token(registered_user):
    """Фикстура для получения токена авторизации"""
    return registered_user["token"] if registered_user else None

@pytest.fixture
def ingredients():
    """Фикстура для получения списка ингредиентов"""
    from utils import get_ingredients
    return get_ingredients()