import pytest
import allure
import requests
from typing import Dict, Any, List
from utils import BASE_URL

@allure.feature('Order Management')
@allure.story('Order Retrieval')
class TestOrderRetrieval:
    
    @allure.title('Получение заказов авторизованным пользователем')
    @allure.description('Проверка получения списка заказов авторизованным пользователем')
    def test_get_orders_with_auth(
        self, 
        registered_user: Dict[str, Any],
        ingredients: List[Dict[str, Any]]
    ) -> None:
        if not ingredients:
            pytest.skip("Нет доступных ингредиентов для теста")
        
        # Сначала создаем заказ для пользователя с валидными ингредиентами
        ingredient_ids = [ing["_id"] for ing in ingredients[:2]]
        response = requests.post(
            f"{BASE_URL}/orders",
            json={"ingredients": ingredient_ids},
            headers={"Authorization": registered_user["token"]}
        )
        
        # ИСПРАВЛЕНО: Проверяем, что заказ создан успешно
        assert response.status_code == 200, f"Заказ не создан: {response.status_code}"
        
        # Теперь получаем список заказов
        response = requests.get(
            f"{BASE_URL}/orders",
            headers={"Authorization": registered_user["token"]}
        )
        
        # Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is True
        assert "orders" in json_response
        assert isinstance(json_response["orders"], list)
        # Должен быть как минимум один заказ (только что созданный)
        assert len(json_response["orders"]) >= 1
    
    @allure.title('Получение заказов неавторизованным пользователем')
    @allure.description('Проверка блокировки доступа к заказам без авторизации')
    def test_get_orders_without_auth(self) -> None:
        response = requests.get(f"{BASE_URL}/orders")
        
        # Проверяем статус-код
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        
        # Проверяем тело ответа
        json_response: Dict[str, Any] = response.json()
        assert json_response["success"] is False
        assert json_response["message"] == "You should be authorised"