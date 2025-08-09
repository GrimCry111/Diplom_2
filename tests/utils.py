import random
import string
import allure

@allure.step("Генерация уникального email для тестов")
def generate_unique_email() -> str:
    """Генерирует уникальный email для тестов"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{random_string}@example.com"

@allure.step("Генерация случайного имени для тестов")
def generate_random_name() -> str:
    """Генерирует случайное имя"""
    return ''.join(random.choices(string.ascii_letters, k=8))