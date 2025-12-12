"""
Примеры тест-кейсов в формате, который ожидается от LLM.
Эти примеры соответствуют шаблонам Jinja2 и используются для настройки промптов.
"""

EXAMPLE_1 = '''
import pytest
import requests
import allure
from typing import Dict, Any

BASE_URL = "https://api.example.com"

@allure.feature("Управление виртуальными машинами")
@allure.title("Тест получения списка виртуальных машин")
def test_get_vms_list():
    """
    Тест на получение списка виртуальных машин.
    Проверить статус код 200 и структуру ответа.
    """
    with allure.step("Отправить GET запрос на /api/v1/vms"):
        response = requests.get(f"{BASE_URL}/api/v1/vms")

    with allure.step("Проверить статус код ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    with allure.step("Проверить структуру ответа"):
        data = response.json()
        assert isinstance(data, list), "Ответ должен быть списком"

        if data:  # Если список не пустой
            first_vm = data[0]
            assert "id" in first_vm, "У ВМ должен быть ID"
            assert "name" in first_vm, "У ВМ должно быть имя"
            assert "status" in first_vm, "У ВМ должен быть статус"

@allure.feature("Управление виртуальными машинами")
@allure.title("Тест создания виртуальной машины")
def test_create_vm():
    """
    Тест на создание виртуальной машины с минимальным набором параметров.
    Проверить статус код 201 и наличие ID в ответе.
    """
    test_data = {
        "name": "test-vm-01",
        "image": "ubuntu-20.04",
        "flavor": "small"
    }

    with allure.step("Подготовить тестовые данные"):
        allure.attach(str(test_data), name="Тестовые данные", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Отправить POST запрос на /api/v1/vms"):
        response = requests.post(
            f"{BASE_URL}/api/v1/vms",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

    with allure.step("Проверить статус код ответа"):
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

    with allure.step("Проверить наличие ID в ответе"):
        created_vm = response.json()
        assert "id" in created_vm, "В ответе должен быть ID созданной ВМ"
        assert created_vm["id"] is not None, "ID не должен быть пустым"

    # Очистка (teardown)
    with allure.step("Удалить созданную ВМ"):
        if "id" in created_vm:
            requests.delete(f"{BASE_URL}/api/v1/vms/{created_vm['id']}")
'''

EXAMPLE_2 = '''
import pytest
import requests
import allure
import uuid

BASE_URL = "https://api.example.com"

@allure.feature("Управление пользователями")
@allure.title("Тест получения пользователя по ID")
def test_get_user_by_id():
    """
    Тест на получение пользователя по ID.
    Проверить статус код 200 и корректность данных в ответе.
    """
    # Сначала создаем тестового пользователя
    user_data = {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com"
    }

    create_response = requests.post(f"{BASE_URL}/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    try:
        with allure.step(f"Отправить GET запрос на /api/v1/users/{user_id}"):
            response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}")

        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить корректность данных в ответе"):
            user = response.json()
            assert user["id"] == user_id
            assert user["username"] == user_data["username"]
            assert user["email"] == user_data["email"]

    finally:
        # Очистка
        requests.delete(f"{BASE_URL}/api/v1/users/{user_id}")

@allure.feature("Управление пользователями")
@allure.title("Тест удаления пользователя")
def test_delete_user():
    """
    Тест на удаление пользователя по ID.
    Проверить статус код 204.
    """
    # Создаем пользователя для удаления
    user_data = {
        "username": f"todelete_{uuid.uuid4().hex[:8]}",
        "email": f"delete_{uuid.uuid4().hex[:8]}@example.com"
    }

    create_response = requests.post(f"{BASE_URL}/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    with allure.step(f"Отправить DELETE запрос на /api/v1/users/{user_id}"):
        response = requests.delete(f"{BASE_URL}/api/v1/users/{user_id}")

    with allure.step("Проверить статус код ответа"):
        assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"

    with allure.step("Проверить, что пользователь действительно удален"):
        get_response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}")
        assert get_response.status_code == 404, "Пользователь должен быть не найден после удаления"
'''

EXAMPLE_3 = '''
import pytest
import requests
import allure
import time

BASE_URL = "https://api.example.com"

@allure.feature("API Health Check")
@allure.title("Тест доступности API")
def test_api_health():
    """
    Базовый тест на доступность API.
    """
    with allure.step("Отправить GET запрос на /health"):
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/health")
        response_time = time.time() - start_time

    with allure.step("Проверить статус код"):
        assert response.status_code == 200

    with allure.step("Проверить время ответа"):
        assert response_time < 2.0, f"Время ответа {response_time:.2f}с превышает лимит 2с"

    with allure.step("Проверить структуру ответа health check"):
        health_data = response.json()
        assert "status" in health_data
        assert health_data["status"] == "healthy"
        assert "timestamp" in health_data
        assert "version" in health_data

@allure.feature("Авторизация")
@allure.title("Тест аутентификации с неверными credentials")
def test_auth_with_invalid_credentials():
    """
    Тест на обработку неверных учетных данных.
    """
    invalid_credentials = {
        "username": "invalid_user",
        "password": "wrong_password"
    }

    with allure.step("Отправить POST запрос на /api/v1/auth/login с неверными данными"):
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=invalid_credentials
        )

    with allure.step("Проверить статус код ошибки"):
        assert response.status_code == 401, "Ожидалась ошибка 401 Unauthorized"

    with allure.step("Проверить сообщение об ошибке"):
        error_data = response.json()
        assert "error" in error_data
        assert "message" in error_data["error"]
'''