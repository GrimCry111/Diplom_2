import requests
import allure
from utils import generate_unique_email, generate_random_name
from urls import REGIST_URL, INGREDIENTS_URL
from typing import Dict, Any, Optional, List

@allure.step("Создание нового пользователя через API")
def create_user() -> Optional[Dict[str, Any]]:
    """Создает нового пользователя и возвращает данные и токен"""
    email = generate_unique_email()
    password = "password123"
    name = generate_random_name()
    
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    
    response = requests.post(f"{REGIST_URL}", json=payload)
    if response.status_code == 200:
        return {
            "email": email,
            "password": password,
            "name": name,
            "token": response.json()["accessToken"],
            "response": response
        }
    return

@allure.step("Получение списка ингредиентов через API")
def get_ingredients() -> List[Dict[str, Any]]:
    """Получает список ингредиентов из API"""
    response = requests.get(f"{INGREDIENTS_URL}")
    return response.json()["data"] if response.status_code == 200 else []