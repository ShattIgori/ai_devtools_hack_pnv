import os
import sys
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from functools import lru_cache
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Добавляем Cloud2 в sys.path для импорта модулей
# sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Удаляем, так как структура изменена

# Импортируем наши модули
try:
    from parser import parse_openapi
    from generator import generate_test_code
    from llm_client import LLMClient
    from gitlab_client import GitLabClient
except ImportError as e:
    print(f"❌ Ошибка импорта модулей в FastAPI: {e}")
    # В реальном приложении это должно быть обработано лучше
    raise RuntimeError(f"Не удалось запустить приложение из-за ошибки импорта: {e}")

# Инициализация клиентов
llm_client = LLMClient()
gitlab_client = GitLabClient()

# Настройка логирования (Задача 8)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="TestOps Copilot Backend",
    description="API для генерации тестов из OpenAPI и интеграции с GitLab.",
    version="1.0.0"
)

# Настройка CORS (Задача 6)
# Разрешаем запросы с любого источника для простоты демо
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommitRequest(BaseModel):
    test_code: str
    repo_url: str
    file_name: str = "generated_test.py"

class UITestRequest(BaseModel):
    requirements: str


# Кэширование запросов к LLM (Задача 8) - lru_cache не работает с async,
# поэтому используем простую заглушку для демонстрации логики.
# В реальном приложении нужно использовать async-совместимый кэш (например, aiocache).
# Для исправления ошибки asyncio.run() мы вызываем асинхронную функцию напрямую.

@app.post("/generate/ui")
async def generate_ui_tests(request: UITestRequest):
    """
    Генерирует UI тесты на основе текстовых требований, используя LLM.
    """
    logger.info(f"Запрос на генерацию UI теста: {request.requirements[:50]}...")
    try:
        # Вызываем асинхронную функцию напрямую с await
        tests = await llm_client.generate_test(request.requirements)
        logger.info("Генерация UI теста завершена.")
        return JSONResponse(content={"tests": tests})
    except Exception as e:
        logger.error(f"Ошибка генерации UI тестов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации UI тестов: {e}")

@app.post("/generate/api")
async def generate_api_tests(openapi_spec: UploadFile = File(...)):
    """
    Генерирует API тесты на основе загруженной OpenAPI спецификации.
    """
    try:
        # 1. Чтение и парсинг спецификации
        spec_content = await openapi_spec.read()
        
        # Попытка декодировать как текст (для YAML/JSON)
        try:
            spec_text = spec_content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Не удалось декодировать файл как текст (ожидается JSON/YAML).")

        # Парсинг
        try:
            parsed_data = parse_openapi(spec_text)
        except Exception as parse_error:
            # Обработка ошибки невалидного OpenAPI файла (Задача 8)
            raise HTTPException(status_code=400, detail=f"Невалидный OpenAPI файл: {parse_error}")
        
        if not parsed_data:
            raise HTTPException(status_code=400, detail="Не удалось распарсить OpenAPI спецификацию. Проверьте формат.")

        # 2. Генерация сценариев (для LLM)
        # В реальной жизни здесь будет вызов LLM для генерации кода
        # Для MVP мы сгенерируем один тестовый файл из первого эндпоинта
        
        first_endpoint = parsed_data[0]
        
        api_context = {
            "story_name": f"API Test for {first_endpoint['path']}",
            "ClassName": f"Test{first_endpoint['method']}{first_endpoint['path'].replace('/', '_').replace('{', '').replace('}', '').title()}",
            "test_title": f"Проверка {first_endpoint['method']} {first_endpoint['path']}",
            "method_name": f"test_{first_endpoint['method'].lower()}",
            "operation_id": first_endpoint.get('operationId', 'N/A'),
            "method": first_endpoint['method'],
            "path": first_endpoint['path'],
            "base_url": "https://api.example.com", # Заглушка
            "expected_status_code": 200 # Заглушка
        }
        
        tests = generate_test_code('api_test_template.j2', api_context)
        
        return JSONResponse(content={"tests": tests, "parsed_endpoints": len(parsed_data)})
    
    except HTTPException:
        # Перебрасываем HTTPException, чтобы FastAPI обработал их
        raise
    except Exception as e:
        # Логирование и возврат общей ошибки
        print(f"Критическая ошибка в /generate/api: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")

@app.post("/commit")
async def commit_tests(request: CommitRequest):
    """
    Коммитит сгенерированный тестовый код в репозиторий GitLab.
    """
    try:
        result = gitlab_client.commit_to_gitlab(
            test_code=request.test_code,
            repo_url=request.repo_url,
            file_name=request.file_name
        )
        # Обработка случая, когда токен не установлен (заглушка)
        if result.get("status") == "simulated":
            return JSONResponse(content=result, status_code=202) # Accepted, но с предупреждением
            
        return JSONResponse(content=result)
    except RuntimeError as e:
        # Обработка ошибки недоступности GitLab (Задача 8)
        raise HTTPException(status_code=503, detail=f"GitLab недоступен или ошибка аутентификации: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка коммита в GitLab: {e}")

# Дополнительный endpoint для проверки здоровья
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "TestOps Copilot Backend is running."}

# Запуск Uvicorn (для локального запуска)
if __name__ == "__main__":
    import uvicorn
    # os.chdir(os.path.dirname(os.path.abspath(__file__))) # Удаляем, так как структура изменена
    uvicorn.run(app, host="0.0.0.0", port=8000)
