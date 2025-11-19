import jsonschema

from .schemas.pet_schema import PET_SCHEMA
import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            pauload = {"id": 9999, "name": "Non-existent Pet", "status": "available"}
            response = requests.put(url=f"{BASE_URL}/pet", json=pauload)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert (
                response.text == "Pet not found"
            ), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ответа"):
            assert (
                response.text == "Pet not found"
            ), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Создание нового питомца")
    def test_create_pet(self):
        with allure.step("Подготовка данный на создание питомца"):
            payload = {"id": 1, "name": "doggie", "status": "available"}
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            jsonschema.validate(instance=response.json(), schema=PET_SCHEMA)
            response_json = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Пришел не корректный статус код"

        with allure.step("Проверка параметров ответа на создание питомца"):
            assert (
                response_json["id"] == payload["id"]
            ), "id запроса != параметрам ответа "
            assert (
                response_json["name"] == payload["name"]
            ), "name запроса != параметрам ответа "
            assert (
                response_json["status"] == payload["status"]
            ), "status запроса != параметрам ответа"

    @allure.title("Добавление нового питомца с всеми полями")
    def test_create_full_body_params(self):
        with allure.step("Подготовка данный на создание питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available",
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            jsonschema.validate(instance=response.json(), schema=PET_SCHEMA)
            response_json = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Пришел не корректный статус код"

        with allure.step("Проверка параметров ответа на создание питомца"):
            assert (
                response_json["id"] == payload["id"]
            ), "id запроса не равен соответствующему параметру в ответе"
            assert (
                response_json["name"] == payload["name"]
            ), "name запросане равен соответствующему параметру в ответе"
            assert (
                response_json["status"] == payload["status"]
            ), "status запроса не равен соответствующему параметру в ответе"
            assert (
                response_json["category"]["id"] == payload["category"]["id"]
            ), "['category']['id'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["category"]["name"] == payload["category"]["name"]
            ), "['category']['name'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["tags"][0]["id"] == payload["tags"][0]["id"]
            ), "['tags']['id'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["tags"][0]["name"] == payload["tags"][0]["name"]
            ), "['tags']['name'] в запросене равен соответствующему параметру в ответе"
            assert (
                response_json["photoUrls"] == payload["photoUrls"]
            ), "['photoUrls'] в запросе не равен соответствующему параметру в ответе"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Пришел не корректный статус код"
            assert (
                response.json()["id"] == pet_id
            ), f"Пришел не корректный ID животного \n Ожидаемый результат: {pet_id} \n Фактический результат: {response.json()['id']}"
