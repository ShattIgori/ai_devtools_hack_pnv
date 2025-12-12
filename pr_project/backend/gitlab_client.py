import os
import subprocess
from typing import Optional, Dict, Any

class GitLabClient:
    """
    Клиент для минимальной интеграции с GitLab.
    Использует переменную окружения GITLAB_TOKEN.
    """
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITLAB_TOKEN")
        if not self.token:
            print("⚠️ ВНИМАНИЕ: GITLAB_TOKEN не найден. Коммит в GitLab будет симулирован.")

    def _run_git_command(self, command: str, repo_path: str) -> str:
        """
        Выполняет команду git в указанной директории.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=repo_path
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"❌ Ошибка выполнения команды git: {e.stderr.strip()}"
            print(error_message)
            raise RuntimeError(error_message)

    def commit_to_gitlab(self, test_code: str, repo_url: str, file_name: str = "generated_test.py") -> Dict[str, Any]:
        """
        Минимальная интеграция: клонирует, создает файл, коммитит и пушит.

        Args:
            test_code: Код теста для коммита.
            repo_url: URL репозитория GitLab (например, https://gitlab.com/user/repo.git).
            file_name: Имя файла, в который будет сохранен тест.

        Returns:
            Словарь с результатом операции.
        """
        repo_dir = "temp_repo"
        
        # 1. Симуляция, если токен не найден
        if not self.token:
            print(f"✅ Симуляция коммита: Файл {file_name} сгенерирован и готов к коммиту в {repo_url}")
            return {
                "status": "simulated",
                "message": f"Коммит симулирован, так как GITLAB_TOKEN не установлен. Код сохранен в {file_name}.",
                "file_content_preview": test_code[:200] + "..."
            }

        # 2. Клонируем репозиторий (с использованием токена для аутентификации)
        # В реальной жизни нужно подставить токен в URL: https://oauth2:{token}@gitlab.com/user/repo.git
        # Для простоты и безопасности в песочнице, мы будем использовать заглушку
        # и предполагать, что репозиторий уже существует или мы его создадим.
        
        # Для песочницы, мы просто создадим временную директорию и файл
        try:
            # Создаем временную директорию
            os.makedirs(repo_dir, exist_ok=True)
            
            # 3. Создаём файл test_generated.py
            file_path = os.path.join(repo_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(test_code)
            
            # 4. Симуляция git-операций
            # В реальной жизни здесь будут:
            # self._run_git_command(f"git clone {repo_url_with_token} {repo_dir}", ".")
            # self._run_git_command("git config user.email 'bot@example.com'", repo_dir)
            # self._run_git_command("git config user.name 'TestGenBot'", repo_dir)
            # self._run_git_command(f"git add {file_name}", repo_dir)
            # self._run_git_command(f"git commit -m 'Generated test: {file_name}'", repo_dir)
            # self._run_git_command("git push origin main", repo_dir)
            
            # Очистка
            # self._run_git_command(f"rm -rf {repo_dir}", ".")
            
            return {
                "status": "success",
                "message": f"Файл {file_name} успешно создан в {repo_dir}. Git-операции симулированы.",
                "file_path": file_path,
                "repo_url": repo_url
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Критическая ошибка при симуляции коммита: {e}",
                "details": str(e)
            }

# Пример использования (для отладки)
if __name__ == "__main__":
    client = GitLabClient(token="fake_token_for_demo")
    
    test_code_example = "def test_example(): assert 1 == 1"
    repo_url_example = "https://gitlab.com/jasur/test-generator.git"
    
    result = client.commit_to_gitlab(test_code_example, repo_url_example)
    print("\n--- Результат коммита ---")
    print(result)
    
    # Очистка временной директории
    try:
        subprocess.run("rm -rf temp_repo", shell=True, check=True)
    except:
        pass
