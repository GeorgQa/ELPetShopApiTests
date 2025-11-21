import allure
import requests
from .schemas.store_schema import STORE_SCHEMA
from .schemas.store_inventory_schema import STORE_INVENTORY_SCHEMA

import jsonschema


BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_store_order(self):
        with allure.step("Подготовка данных на создание заказа"):
            payload = {
                "id": 10,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": False,
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
        with allure.step("Валидация ответа, проверка статус кода и данных"):
            assert (
                response.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
            jsonschema.validate(
                instance=response.json(), schema=STORE_SCHEMA
            ), "Тело ответа не прошло валидацию"
            assert (
                response_json["id"] == payload["id"]
            ), "Параметр: ID заказа в магазине в запросе и ответе совпали"
            assert (
                response_json["petId"] == payload["petId"]
            ), "Параметр: petId заказа в магазине в запросе и ответе совпали"
            assert (
                response_json["quantity"] == payload["quantity"]
            ), "Параметр: QUANTITY заказа в магазине в запросе и ответе совпали"
            assert (
                response_json["status"] == payload["status"]
            ), "Параметр: STATUS заказа в магазине в запросе и ответе совпали"
            assert (
                response_json["complete"] == payload["complete"]
            ), "Параметр: COMPLETE заказа в магазине в запросе и ответе совпали"

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_for_order(self, create_order_for_store):
        with allure.step("Отправка запроса на получение информации, о заказе"):
            response_get = requests.get(
                url=f"{BASE_URL}/store/order/{create_order_for_store['id']}"
            )
        with allure.step("Проверка статус кода и корректности данных"):
            assert (
                response_get.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_get.json()["id"] == create_order_for_store["id"]
            ), f"Ответ содержит не тот ID заказа ожидаемое значение: {create_order_for_store['id']}, фактическое: {response_get.json()['id']}"

    @allure.title("Удаление заказа")
    def test_delete_order(self, create_order_for_store):
        with allure.step("Отправка запроса на удаление заказа"):
            response_delete = requests.delete(
                url=f"{BASE_URL}/store/order/{create_order_for_store['id']}"
            )
            assert (
                response_delete.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
        with allure.step("Отправка запроса на получение заказа"):
            response_get = requests.get(
                url=f"{BASE_URL}/store/order/{create_order_for_store['id']}"
            )
            assert (
                response_get.status_code == 404
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_get.text == "Order not found"
            ), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем  заказе")
    def test_get_info_nonexistent_order(self):
        with allure.step("Отправка запроса на несуществующей заказ"):
            response_get = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статус кода и текста ошибки"):
            assert (
                response_get.status_code == 404
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_get.text == "Order not found"
            ), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_from_store(self):
        with allure.step("Отправка запроса на получение данных"):
            response_get = requests.get(url=f"{BASE_URL}/store/inventory")
            response_get_json = response_get.json()
        with allure.step("Проверка статус кода и валидация ответа"):
            assert (
                response_get.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
        jsonschema.validate(instance=response_get_json , schema=STORE_INVENTORY_SCHEMA ), "Тело ответа не прошло валидацию"
