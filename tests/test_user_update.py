import allure
import requests
import random
import string
from urls import AUTH_URL
from data_text import USER_UPDATE_RESP
from typing import Dict, Any

def generate_random_name() -> str:
    """Генерирует случайное имя"""
    return ''.join(random.choices(string.ascii_letters, k=8))

@allure.feature('User Management')
@allure.story('User Update')
class TestUserUpdate:
    
    @allure.title('Изменение данных пользователя с авторизацией')
    @allure.description('Проверка обновления email и имени авторизованным пользователем')
    def test_update_user_with_auth(self, registered_user: Dict[str, Any]) -> None:
        new_email = f"updated_{registered_user['email']}"
        new_name = generate_random_name()
        
        payload: Dict[str, str] = {
            "email": new_email,
            "name": new_name
        }
        
        response = requests.patch(
            f"{AUTH_URL}",
            json=payload,
            headers={"Authorization": registered_user["token"]}
        )
        
        # Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is True
        assert json_response["user"]["email"] == new_email
        assert json_response["user"]["name"] == new_name
    
    @allure.title('Изменение email пользователя с авторизацией')
    @allure.description('Проверка обновления только email авторизованным пользователем')
    def test_update_user_email_with_auth(self, registered_user: Dict[str, Any]) -> None:
        new_email = f"updated_{registered_user['email']}"
        
        payload: Dict[str, str] = {"email": new_email}
        
        response = requests.patch(
            f"{AUTH_URL}",
            json=payload,
            headers={"Authorization": registered_user["token"]}
        )
        
        # Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is True
        assert json_response["user"]["email"] == new_email
        assert json_response["user"]["name"] == registered_user["name"]
    
    @allure.title('Изменение данных пользователя без авторизации')
    @allure.description('Проверка блокировки изменения данных без токена')
    def test_update_user_without_auth(self, registered_user: Dict[str, Any]) -> None:
        payload: Dict[str, str] = {
            "email": f"updated_{registered_user['email']}",
            "name": generate_random_name()
        }
        
        response = requests.patch(
            f"{AUTH_URL}",
            json=payload
        )
        
        # Проверяем статус-код
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is False
        assert json_response["message"] == USER_UPDATE_RESP