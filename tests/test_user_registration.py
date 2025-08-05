import pytest
import allure
import requests
from typing import Dict, Any
from utils import generate_unique_email, BASE_URL

@allure.feature('User Management')
@allure.story('User Registration')
class TestUserRegistration:
    
    @allure.title('Создание уникального пользователя')
    @allure.description('Проверка успешного создания нового пользователя')
    def test_create_unique_user(self) -> None:
        email = generate_unique_email()
        payload: Dict[str, str] = {
            "email": email,
            "password": "password123",
            "name": "Test User"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is True
        assert "accessToken" in json_response
        # ИСПРАВЛЕНО: Поле называется "refreshToken", а не " refreshToken" (без пробела)
        assert "refreshToken" in json_response
        assert "user" in json_response
        assert json_response["user"]["email"] == email
        assert json_response["user"]["name"] == "Test User"
        
        # Удаляем созданного пользователя
        token = json_response["accessToken"]
        requests.delete(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": token}
        )
    
    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Проверка обработки попытки регистрации существующего пользователя')
    def test_create_existing_user(self, registered_user: Dict[str, Any]) -> None:
        # Используем уже зарегистрированного пользователя
        payload: Dict[str, str] = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is False
        assert json_response["message"] == "User already exists"
    
    @allure.title('Создание пользователя без одного обязательного поля')
    @allure.description('Проверка обработки запроса с отсутствующим email')
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_create_user_missing_field(self, missing_field: str) -> None:
        email = generate_unique_email()
        payload: Dict[str, str] = {
            "email": email,
            "password": "password123",
            "name": "Test User"
        }
        
        # Удаляем одно обязательное поле
        payload.pop(missing_field)
        
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is False
        assert "message" in json_response