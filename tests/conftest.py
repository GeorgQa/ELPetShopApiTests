import time

from .schemas.store_schema import STORE_SCHEMA
import jsonschema
import pytest
import requests


BASE_URL = "http://5.181.109.28:9090/api/v3"


@pytest.fixture(scope="class")
def create_pet():
    """Фикстура для создания питомца."""
    payload = {
        "id": 165,
        "name": "doggie",
        "category": {"id": 1, "name": "Dogs"},
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available",
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert  response.status_code == 200 , "Пришел не корректный статус код"
    return  response.json()


@pytest.fixture(scope="class")
def create_order_for_store():
    """Фистура для создания заказа в магазине"""

    payload = {
                    "id": 101,
                    "petId": 1,
                    "quantity": 1,
                    "status": "placed",
                    "complete": False,
                }
    response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
    assert (response.status_code == 200), "Статус код ответа не совпал с ожидаемым"
    jsonschema.validate(
        instance=response.json(), schema=STORE_SCHEMA
    ), "Тело ответа не прошло валидацию"
    return  response.json()

