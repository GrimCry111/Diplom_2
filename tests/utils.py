import requests
import random
import string
from typing import Dict, Any, Optional, List

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

def generate_unique_email() -> str:
    """Генерирует уникальный email для тестов"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{random_string}@example.com"

def generate_random_name() -> str:
    """Генерирует случайное имя"""
    return ''.join(random.choices(string.ascii_letters, k=8))

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
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    if response.status_code == 200:
        return {
            "email": email,
            "password": password,
            "name": name,
            "token": response.json()["accessToken"],
            "response": response
        }
    return None

def get_ingredients() -> List[Dict[str, Any]]:
    """Получает список ингредиентов из API"""
    response = requests.get(f"{BASE_URL}/ingredients")
    return response.json()["data"] if response.status_code == 200 else []