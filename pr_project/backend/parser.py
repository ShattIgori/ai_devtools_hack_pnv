import json
import os
from typing import Dict, List, Any, Optional


def parse_openapi(file_path: str) -> List[Dict[str, Any]]:
    """
    Парсит OpenAPI файл в формате JSON или YAML.

    Поддерживаемые расширения:
    - .json, .yaml, .yml для явного указания формата
    - Автоопределение формата по содержимому для файлов без расширения

    Args:
        file_path: Путь к OpenAPI файлу

    Returns:
        Список словарей с данными эндпоинтов

    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если файл не является валидным JSON или YAML
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Читаем содержимое файла
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    spec = None

    # Определяем формат по расширению файла
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext in ['.json']:
        # Парсим как JSON
        try:
            spec = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")

    elif file_ext in ['.yaml', '.yml']:
        # Парсим как YAML
        try:
            import yaml
            spec = yaml.safe_load(content)
        except ImportError:
            raise ImportError("Для парсинга YAML файлов требуется библиотека PyYAML. "
                              "Установите: pip install pyyaml")
        except yaml.YAMLError as e:
            raise ValueError(f"Ошибка парсинга YAML: {e}")

    else:
        # Автоопределение формата по содержимому
        try:
            # Пробуем сначала как JSON
            spec = json.loads(content)
            print(f"   Формат определен как JSON (автоопределение)")
        except json.JSONDecodeError:
            # Пробуем как YAML
            try:
                import yaml
                spec = yaml.safe_load(content)
                print(f"   Формат определен как YAML (автоопределение)")
            except ImportError:
                raise ImportError("Не удалось определить формат. "
                                  "Установите PyYAML для поддержки YAML: pip install pyyaml")
            except yaml.YAMLError:
                raise ValueError("Не удалось определить формат файла. "
                                 "Поддерживаются только JSON и YAML.")

    # Проверяем, что это OpenAPI спецификация
    if not isinstance(spec, dict):
        raise ValueError("OpenAPI файл должен содержать словарь (объект)")

    if 'openapi' not in spec and 'swagger' not in spec:
        raise ValueError("Файл не является OpenAPI спецификацией. "
                         "Отсутствует поле 'openapi' или 'swagger'")

    # Выводим информацию о версии
    if 'openapi' in spec:
        print(f"   Версия OpenAPI: {spec.get('openapi')}")
    elif 'swagger' in spec:
        print(f"   Версия Swagger: {spec.get('swagger')}")

    endpoints = []

    # Извлекаем базовый URL
    base_url = ""
    if 'servers' in spec and spec['servers']:
        base_url = spec['servers'][0].get('url', '')
        print(f"   Базовый URL: {base_url}")

    # Обрабатываем пути
    paths = spec.get('paths', {})
    if not paths:
        print("   Предупреждение: в спецификации нет путей (paths)")
        return endpoints

    print(f"   Найдено путей (paths): {len(paths)}")

    endpoint_count = 0
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        for method, operation in path_item.items():
            method_lower = method.lower()
            if method_lower not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                continue

            endpoint_count += 1
            endpoint_data = {
                'path': path,
                'full_path': f"{base_url}{path}" if base_url else path,
                'method': method.upper(),
                'operation_id': operation.get('operationId', ''),
                'summary': operation.get('summary', ''),
                'description': operation.get('description', ''),
                'parameters': [],
                'has_request_body': False,
                'tags': operation.get('tags', []),
                'responses': list(operation.get('responses', {}).keys()) if operation.get('responses') else []
            }

            # Обрабатываем параметры
            for param in operation.get('parameters', []):
                if isinstance(param, dict):
                    param_data = {
                        'name': param.get('name', ''),
                        'in': param.get('in', ''),
                        'required': param.get('required', False),
                        'type': param.get('schema', {}).get('type', 'string'),
                        'description': param.get('description', '')
                    }
                    endpoint_data['parameters'].append(param_data)

            # Проверяем наличие requestBody
            if 'requestBody' in operation:
                endpoint_data['has_request_body'] = True

            endpoints.append(endpoint_data)

    # Сортируем для удобства
    endpoints.sort(key=lambda x: (x['path'], x['method']))

    print(f"   Обработано эндпоинтов: {endpoint_count}")

    return endpoints


def save_parsed_to_json(endpoints: List[Dict[str, Any]], output_file: str = 'sample_parsed_api.json'):
    """
    Сохраняет результат парсинга в JSON файл.

    Args:
        endpoints: Список эндпоинтов
        output_file: Имя выходного файла
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(endpoints, f, indent=2, ensure_ascii=False, default=str)

    print(f"   Результат сохранен в: {output_file}")
    return output_file


def create_sample_yaml_file():
    """
    Создает пример OpenAPI файла в формате YAML для тестирования.
    """
    yaml_content = """openapi: 3.0.0
info:
  title: Sample API (YAML format)
  version: 1.0.0
  description: Пример OpenAPI спецификации в формате YAML
servers:
  - url: https://api.example.com
    description: Production server
paths:
  /api/v1/users:
    get:
      summary: Get users list
      operationId: getUsers
      responses:
        '200':
          description: Success
    post:
      summary: Create user
      operationId: createUser
      requestBody:
        required: true
      responses:
        '201':
          description: Created
  /api/v1/users/{id}:
    get:
      summary: Get user by ID
      operationId: getUserById
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
"""

    with open('sample_openapi.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    print("Создан sample_openapi.yaml для тестирования парсера YAML")
    return 'sample_openapi.yaml'


# Пример тестирования разных форматов
if __name__ == "__main__":
    print("🔧 Тестирование парсера OpenAPI")
    print("=" * 50)

    # Создаем тестовые файлы
    create_sample_yaml_file()

    # Тестируем разные форматы
    test_files = [
        ('sample_openapi.json', 'JSON'),
        ('sample_openapi.yaml', 'YAML'),
    ]

    for file_name, format_name in test_files:
        if os.path.exists(file_name):
            print(f"\n📄 Парсинг {format_name} файла: {file_name}")
            print("-" * 40)
            try:
                endpoints = parse_openapi(file_name)
                print(f"✅ Успешно! Найдено эндпоинтов: {len(endpoints)}")

                # Сохраняем результат
                output_file = file_name.replace('.json', '_parsed.json').replace('.yaml', '_parsed.json')
                save_parsed_to_json(endpoints, output_file)

            except Exception as e:
                print(f"❌ Ошибка: {e}")
        else:
            print(f"\n⚠️  Файл {file_name} не найден")