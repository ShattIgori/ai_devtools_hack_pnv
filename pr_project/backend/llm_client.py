import os
import asyncio
from typing import Optional
from openai import AsyncOpenAI, APIStatusError, APIConnectionError

# Заглушка для тестового кода на случай недоступности LLM API
FALLBACK_TEST_CODE = """
# Fallback Test Case - LLM API is unavailable
import allure
import pytest

@allure.feature("Fallback Feature")
@allure.story("LLM API Unavailable")
class TestFallback:
    @allure.title("Сгенерированный тест-кейс (Заглушка)")
    def test_fallback_case(self):
        with allure.step("Arrange"):
            # Инициализация: LLM API недоступен, используется шаблонная заглушка
            pass
        with allure.step("Act"):
            # Выполнение действия: Симуляция генерации теста
            pass
        with allure.step("Assert"):
            # Проверка: Успешное возвращение заглушки
            assert True
"""

# Предполагаемый базовый URL для Cloud.ru Evolution Model (на основе документации)
# В реальном проекте это должно быть получено из документации Cloud.ru
# Используем заглушку, так как точный URL не найден, но это позволит использовать AsyncOpenAI
# Пользователь должен будет установить правильный URL через переменную окружения или в коде
CLOUD_RU_API_BASE = os.getenv("CLOUD_RU_API_BASE", "https://api.cloud.ru/evolution/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3-8b-instruct") # Используем популярную модель для примера

class LLMClient:
    """
    Клиент для взаимодействия с Cloud.ru Evolution Model API.
    Использует переменную окружения CLOUD_RU_API_KEY.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLOUD_RU_API_KEY")
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️ ВНИМАНИЕ: CLOUD_RU_API_KEY не найден. LLMClient будет использовать заглушку.")
            self.client = None
        else:
            # Инициализация AsyncOpenAI клиента
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=CLOUD_RU_API_BASE
            )
            print(f"✅ LLMClient инициализирован. Base URL: {CLOUD_RU_API_BASE}")

    async def generate_test(self, requirement: str) -> str:
        """
        Генерирует тест-кейс на основе требования, используя LLM.

        Args:
            requirement: Требование для генерации тест-кейса.

        Returns:
            Сгенерированный код тест-кейса в формате Allure.
        """
        if not self.client:
            # Возврат шаблонных тестов (заглушка)
            return FALLBACK_TEST_CODE

        # Формирование промпта
        system_prompt = (
            "Ты — эксперт по автоматизации тестирования. Твоя задача — сгенерировать "
            "тестовый код на Python с использованием pytest и Allure-отчетов. "
            "Код должен быть готов к выполнению. Не добавляй пояснений, только чистый код."
        )
        
        user_prompt = (
            f"Сгенерируй один полный тест-кейс на Python для следующего требования: '{requirement}'. "
            "Используй декораторы @allure.feature, @allure.story, @allure.title и шаги allure.step. "
            "Тестовая функция должна начинаться с 'test_'. "
            "Если это API тест, используй библиотеку 'requests'. "
            "Если это UI тест, используй заглушки для действий."
        )

        # Вызов API
        try:
            chat_completion = await self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            
            # Извлечение сгенерированного текста
            generated_text = chat_completion.choices[0].message.content
            
            # Очистка от лишних символов (например, markdown-блоков)
            if generated_text.startswith("```python"):
                generated_text = generated_text.replace("```python", "").strip()
            if generated_text.endswith("```"):
                generated_text = generated_text.replace("```", "").strip()
                
            return generated_text
            
        except (APIStatusError, APIConnectionError) as e:
            print(f"❌ Ошибка API ({type(e).__name__}): {e}. Используется заглушка.")
            return FALLBACK_TEST_CODE
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}. Используется заглушка.")
            return FALLBACK_TEST_CODE

# Пример использования (для отладки)
if __name__ == "__main__":
    async def main():
        # Инициализация без ключа для демонстрации заглушки
        client = LLMClient(api_key=None)
        test_code = await client.generate_test("Проверить, что калькулятор цен корректно считает стоимость ВМ с 4 ядрами и 8 ГБ ОЗУ.")
        print("\n--- Сгенерированный код (Заглушка) ---")
        print(test_code)
        
        # Инициализация с фейковым ключом для демонстрации реального вызова (если бы был доступ)
        # client_real = LLMClient(api_key="FAKE_KEY_FOR_DEMO")
        # test_code_real = await client_real.generate_test("Проверить API /users/{id} на возврат 404 для несуществующего пользователя.")
        # print("\n--- Сгенерированный код (Реальный вызов) ---")
        # print(test_code_real)

    # Запуск асинхронной функции
    asyncio.run(main())
