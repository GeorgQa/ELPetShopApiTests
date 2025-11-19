from http.client import responses

import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url= f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса кода"):
            assert response.status_code == 200 , "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert  response.text == "Pet deleted" , "Текст ошибки не соапал с ожидаемым"

    @allure.title("Попытка обновить не существующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            pauload = {
                "id": 9999, "name": "Non-existent Pet", "status":"available"
            }
            response = requests.put(url= f"{BASE_URL}/pet", json= pauload)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"







