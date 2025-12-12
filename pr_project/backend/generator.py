from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
import os

# Настройка Jinja2
# Указываем, что шаблоны находятся в поддиректории 'templates'
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))


def generate_scenarios_from_openapi(parsed_data: List[Dict[str, Any]]) -> List[str]:
    """
    Генерирует текстовые сценарии тестов из распарсенных данных OpenAPI.

    Args:
        parsed_data: Данные от парсера OpenAPI

    Returns:
        Список текстовых описаний сценариев тестов
    """
    scenarios = []

    for endpoint in parsed_data:
        path = endpoint['path']
        method = endpoint['method']
        has_params = len(endpoint['parameters']) > 0
        has_body = endpoint['has_request_body']

        # Определяем тип операции по пути и методу
        path_lower = path.lower()
        last_segment = path.split('/')[-1]

        if method == 'GET':
            if '{' in path:  # Есть path параметр
                scenarios.append(
                    f"Тест на получение {get_resource_name(path)} по ID. Проверить статус код 200 и корректность данных в ответе.")
            else:
                scenarios.append(
                    f"Тест на получение списка {get_resource_name(path)}. Проверить статус код 200 и структуру ответа (массив объектов).")

        elif method == 'POST':
            if has_body:
                scenarios.append(
                    f"Тест на создание {get_resource_name(path)} с минимальным набором параметров. Проверить статус код 201 и наличие ID в ответе.")
            else:
                scenarios.append(f"Тест на вызов операции {path}. Проверить статус код 200 или 201.")

        elif method == 'PUT':
            if has_body:
                scenarios.append(
                    f"Тест на обновление {get_resource_name(path)} по ID. Проверить статус код 200 и корректность обновленных данных.")

        elif method == 'DELETE':
            if '{' in path:
                scenarios.append(f"Тест на удаление {get_resource_name(path)} по ID. Проверить статус код 204 или 200.")
            else:
                scenarios.append(f"Тест на массовое удаление {get_resource_name(path)}. Проверить статус код 204.")

        elif method == 'PATCH':
            scenarios.append(f"Тест на частичное обновление {get_resource_name(path)} по ID. Проверить статус код 200.")

    return scenarios


def get_resource_name(path: str) -> str:
    """
    Извлекает имя ресурса из пути.
    """
    # Удаляем параметры пути
    path = path.split('{')[0]

    # Получаем последний значимый сегмент
    segments = [s for s in path.split('/') if s and not s.startswith('api')]

    if segments:
        resource = segments[-1]
        # Приводим к читаемому виду
        resource = resource.replace('-', ' ').replace('_', ' ')
        if resource.endswith('s'):
            resource = resource[:-1]  # Убираем множественное число
        return resource
    return "ресурса"


def generate_test_code(template_name: str, context: Dict[str, Any]) -> str:
    """
    Генерирует код теста, используя Jinja2 шаблон.

    Args:
        template_name: Имя шаблона (например, 'ui_test_template.j2').
        context: Словарь с данными для заполнения шаблона.

    Returns:
        Сгенерированный код теста.
    """
    try:
        template = env.get_template(template_name)
        return template.render(context)
    except Exception as e:
        return f"# Ошибка генерации теста: {e}"


# Дополнительная функция для более структурированного вывода
def generate_detailed_scenarios(parsed_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Генерирует детализированные сценарии с дополнительной информацией.
    """
    detailed_scenarios = []

    for endpoint in parsed_data:
        scenario = {
            'title': f"{endpoint['method']} {endpoint['path']}",
            'description': generate_scenario_description(endpoint),
            'test_steps': generate_test_steps(endpoint),
            'expected_results': generate_expected_results(endpoint)
        }
        detailed_scenarios.append(scenario)

    return detailed_scenarios


def generate_scenario_description(endpoint: Dict[str, Any]) -> str:
    """Генерирует описание сценария"""
    method = endpoint['method']
    path = endpoint['path']

    descriptions = {
        'GET': f"Получение данных из {path}",
        'POST': f"Создание новой записи через {path}",
        'PUT': f"Полное обновление записи через {path}",
        'DELETE': f"Удаление записи через {path}",
        'PATCH': f"Частичное обновление записи через {path}"
    }

    return descriptions.get(method, f"Тестирование {method} запроса к {path}")


def generate_test_steps(endpoint: Dict[str, Any]) -> List[str]:
    """Генерирует шаги теста"""
    steps = [
        f"1. Подготовить тестовые данные",
        f"2. Отправить {endpoint['method']} запрос на {endpoint['path']}",
    ]

    if endpoint['parameters']:
        steps.append(f"3. Передать параметры: {[p['name'] for p in endpoint['parameters']]}")

    if endpoint['has_request_body']:
        steps.append(f"4. Передать тело запроса с минимальными данными")

    steps.append(f"5. Получить и проверить ответ")

    return steps


def generate_expected_results(endpoint: Dict[str, Any]) -> List[str]:
    """Генерирует ожидаемые результаты"""
    expected = []

    # Определяем ожидаемый статус код
    status_codes = {
        'GET': '200',
        'POST': '201',
        'PUT': '200',
        'DELETE': '204 или 200',
        'PATCH': '200'
    }

    expected.append(f"Статус код: {status_codes.get(endpoint['method'], '2xx')}")

    if endpoint['method'] == 'GET' and '{' not in endpoint['path']:
        expected.append("Ответ содержит массив данных")
    elif endpoint['method'] == 'POST':
        expected.append("Ответ содержит ID созданного ресурса")
    elif endpoint['method'] == 'DELETE':
        expected.append("Ресурс успешно удален")

    expected.append("Структура ответа соответствует спецификации")

    return expected
