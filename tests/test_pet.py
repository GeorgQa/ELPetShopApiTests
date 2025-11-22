import jsonschema
import pytest

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
            assert (
                response.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"

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
            assert (
                response.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"

        with allure.step("Проверка параметров ответа на создание питомца"):
            assert (
                response_json["id"] == payload["id"]
            ), "ID запроса != параметрам ответа "
            assert (
                response_json["name"] == payload["name"]
            ), "NAME запроса != параметрам ответа "
            assert (
                response_json["status"] == payload["status"]
            ), "STATUS запроса != параметрам ответа"

    @allure.title("Добавление нового питомца с всеми полями")
    def test_create_full_body_params(self, create_pet):
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
            assert (
                response.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"

        with allure.step("Проверка параметров ответа на создание питомца"):
            assert (
                response_json["id"] == payload["id"]
            ), "ID запроса не равен соответствующему параметру в ответе"
            assert (
                response_json["name"] == payload["name"]
            ), "NAME запроса не равен соответствующему параметру в ответе"
            assert (
                response_json["status"] == payload["status"]
            ), "STATUS запроса не равен соответствующему параметру в ответе"
            assert (
                response_json["category"]["id"] == payload["category"]["id"]
            ), "['CATEGORY']['ID'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["category"]["name"] == payload["category"]["name"]
            ), "['CATEGORY']['NAME'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["tags"][0]["id"] == payload["tags"][0]["id"]
            ), "['TAGS']['ID'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["tags"][0]["name"] == payload["tags"][0]["name"]
            ), "['TAGS']['NAME'] в запросе не равен соответствующему параметру в ответе"
            assert (
                response_json["photoUrls"] == payload["photoUrls"]
            ), "PHOTOURLS в запросе не равен соответствующему параметру в ответе"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert (
                response.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response.json()["id"] == pet_id
            ), f"Пришел не корректный ID животного \n Ожидаемый результат: {pet_id} \n Фактический результат: {response.json()['id']}"

    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("Получение ID созданного питомце"):
            pet_id = create_pet["id"]
        with allure.step("Подготовка данных для изменения питомца"):
            payload_data_for_pet_update = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold",
            }
        with allure.step("Валидация тестовых данных по json-schema"):
            jsonschema.validate(instance=create_pet, schema=PET_SCHEMA)
        with allure.step("Отправка запроса на изменение животного"):
            response_update = requests.put(
                f"{BASE_URL}/pet", json=payload_data_for_pet_update
            )
            response_update_json = response_update.json()
            assert (
                response_update.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_update_json["id"] == payload_data_for_pet_update["id"]
            ), "ID животного после обновления не равен ID до обновления"
            assert (
                response_update_json["name"] == payload_data_for_pet_update["name"]
            ), "NAME животного после обновления не равно ожидаемому"
            assert (
                response_update_json["status"] == payload_data_for_pet_update["status"]
            ), "STATUS животного после обновления не равен ожидаемому"

    @allure.title("Удаление существующего питомца")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомце"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на удаление питомца"):
            response_delete = requests.delete(f"{BASE_URL}/pet/{pet_id}")
            assert (
                response_delete.status_code == 200
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_delete.text == "Pet deleted"
            ), "Текст ошибки не совпал с ожидаемым"
        with allure.step("Отправка запроса на получение питомца после удаления"):
            response_get_after_delete = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert (
                response_get_after_delete.status_code == 404
            ), "Статус код ответа не совпал с ожидаемым"
            assert (
                response_get_after_delete.text == "Pet not found"
            ), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            (" ", 400),
            ("random_params", 400),
        ],
    )
    def test_get_pet_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response_get = requests.get(
                f"{BASE_URL}/pet/findByStatus", params={"status": f"{status}"}
            )
        with allure.step("Проверка статус кода и формата ответа"):
            assert (
                response_get.status_code == expected_status_code
            ), f"Статус код ответа: {response_get.status_code} не совпал с ожидаемым: {expected_status_code}"
            if response_get.status_code == 200:
                assert isinstance(response_get.json(), list)
            elif response_get.status_code == 400:
                assert (
                    response_get.json()["message"]
                    == f"Input error: query parameter `status value `{status}` is not in the allowable values `[available, pending, sold]`"
                )
            else:
                f"При получение списка питомцев по status: {status}, возникла непредвиденная ошибка"
