🔧 РЕШЕНИЕ ПРОБЛЕМЫ EXIT CODE 127

## Диагностика проблемы:
Exit code 127 = "Command not found" - означает, что Azure App Service не может найти или выполнить команду запуска.

## Решение:

### 1. Проверьте настройки в Azure Portal
В Azure Portal > App Service > Configuration > General Settings:

**Startup Command:**
```
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**ИЛИ для gunicorn:**
```
python -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --timeout 600
```

### 2. Альтернативный способ - через startup.sh
Если используете startup.sh, убедитесь что он исполняемый:

В Configuration > General Settings > Startup Command:
```
/bin/bash startup.sh
```

### 3. Отладочная версия
Временно используйте main_debug.py для тестирования:

Startup Command:
```
python main_debug.py
```

### 4. Простые требования
Используйте requirements_simple.txt (без версий):
```
fastapi
uvicorn[standard]
python-dotenv
pydantic
gunicorn
httpx
aiofiles
python-multipart
aiohttp
```

### 5. Переменные окружения
Убедитесь, что все переменные настроены:
```
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://advokatopenai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_SEARCH_ENDPOINT=https://advokatsearch123.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key
AZURE_SEARCH_INDEX_NAME=rag-1752686975655
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### 6. Проверка после развертывания
1. Проверьте логи: `az webapp log tail --name aiadvokatweb --resource-group your-rg`
2. Тестируйте endpoints:
   - `/health` - проверка работы
   - `/debug` - информация о среде (если используете main_debug.py)
   - `/` - главная страница

### 7. Если все еще не работает
1. Используйте отладочную версию (main_debug.py)
2. Проверьте, что Python 3.11 используется корректно
3. Убедитесь, что все файлы загружены правильно

## Рекомендованная последовательность:
1. **Сначала** попробуйте простую команду запуска: `python main_debug.py`
2. **Затем** перейдите на полную версию: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
3. **Наконец** используйте gunicorn для продакшена

Это должно решить проблему с exit code 127!
