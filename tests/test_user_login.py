import pytest
import allure
import requests
from utils import generate_unique_email, BASE_URL

@allure.feature('User Management')
@allure.story('User Login')
class TestUserLogin:
    
    @allure.title('Логин под существующим пользователем')
    @allure.description('Проверка успешной авторизации зарегистрированного пользователя')
    def test_login_existing_user(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response = response.json()
        assert json_response["success"] is True
        assert "accessToken" in json_response
        assert "user" in json_response
        assert json_response["user"]["email"] == registered_user["email"]
        assert json_response["user"]["name"] == registered_user["name"]
    
    @allure.title('Логин с неверным логином и паролем')
    @allure.description('Проверка обработки неверных учетных данных')
    @pytest.mark.parametrize("email,password", [
        (generate_unique_email(), "wrong_password"),
        ("nonexistent@example.com", "password123")
    ])
    def test_login_with_invalid_credentials(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login", json=payload)
        
        # Проверяем статус-код
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response = response.json()
        assert json_response["success"] is False
        assert json_response["message"] == "email or password are incorrect"