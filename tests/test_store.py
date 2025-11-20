import allure
import requests
from .schemas.store_schema import STORE_SCHEMA
import jsonschema

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_store_order(self):
        with allure.step("Подготовка данных на создание order"):
            payload = {"id": 1, "petId": 1, "quantity": 1, "status": "placed", "complete": False}
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url= f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
        with allure.step("Валидация ответа, проверка статус кода и данных"):
            assert  response.status_code == 200 ,"Статус код ответа не совпал с ожидаемым"
            jsonschema.validate(instance=response.json(),schema= STORE_SCHEMA), "Тело ответа не прошло валидацию"
            assert  response_json["id"] == payload["id"] , "Параметр: ID заказа в магазине в запросе и ответе совпали"
            assert  response_json["petId"] == payload["petId"] , "Параметр: petId заказа в магазине в запросе и ответе совпали"
            assert  response_json["quantity"] == payload["quantity"] , "Параметр: QUANTITY заказа в магазине в запросе и ответе совпали"
            assert  response_json["status"] == payload["status"] ,"Параметр: STATUS заказа в магазине в запросе и ответе совпали"
            assert response_json["complete"] == payload["complete"] , "Параметр: COMPLETE заказа в магазине в запросе и ответе совпали"