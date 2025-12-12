import re
from typing import List, Tuple


def validate_test_code(code: str) -> Tuple[bool, List[str]]:
    """
    Простая валидация тестового кода.

    Args:
        code: Код теста на Python

    Returns:
        Кортеж (валиден ли код, список ошибок/предупреждений)
    """
    errors = []
    warnings = []

    # Критические проверки для демо
    if "@allure" not in code.lower():
        errors.append("Код не содержит декораторов Allure")

    if "def test_" not in code:
        errors.append("Не найдено ни одной тестовой функции (должно начинаться с 'def test_')")

    # Предупреждения
    if "import requests" not in code and "from requests" not in code:
        warnings.append("Не обнаружен импорт requests. Убедитесь, что используете HTTP-клиент")

    if "assert" not in code:
        warnings.append("Код не содержит assert-проверок")

    # Проверка синтаксиса Python (базовая)
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        errors.append(f"Синтаксическая ошибка в коде: {e}")

    is_valid = len(errors) == 0

    return is_valid, errors + warnings


def extract_test_functions(code: str) -> List[dict]:
    """
    Извлекает информацию о тестовых функциях из кода.
    """
    functions = []
    pattern = r'def (test_\w+)\s*\([^)]*\)\s*:'

    matches = re.finditer(pattern, code)
    for match in matches:
        func_name = match.group(1)
        # Ищем декораторы перед функцией
        start_pos = max(0, match.start() - 200)
        decorators = re.findall(r'@\w+', code[start_pos:match.start()])

        functions.append({
            'name': func_name,
            'decorators': decorators,
            'has_allure': any('allure' in d.lower() for d in decorators)
        })

    return functions