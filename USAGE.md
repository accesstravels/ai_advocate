# Пример использования Azure AI Avatar Configuration Service

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка переменных окружения

### Вариант 1: Использование .env файла
```bash
# Скопируйте .env.example в .env
copy .env.example .env

# Отредактируйте .env файл с вашими значениями
```

### Вариант 2: Установка через системные переменные (Windows)
```cmd
set AZURE_SPEECH_KEY=your-speech-key
set AZURE_SPEECH_REGION=eastus2
set AZURE_OPENAI_KEY=your-openai-key
set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
set AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### Вариант 3: Использование PowerShell
```powershell
$env:AZURE_SPEECH_KEY = "your-speech-key"
$env:AZURE_SPEECH_REGION = "eastus2"
$env:AZURE_OPENAI_KEY = "your-openai-key"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
```

## Шаг 3: Запуск приложения

### Для разработки:
```bash
python main.py
```

### Для продакшена:
```bash
# Установите переменную окружения
set ENVIRONMENT=production

# Запустите с gunicorn
gunicorn --bind 0.0.0.0:8000 main:app --worker-class uvicorn.workers.UvicornWorker
```

## Шаг 4: Использование API

### Получение конфигурации:
```javascript
// В вашем frontend приложении
fetch('/config')
  .then(response => response.json())
  .then(config => {
    // Используйте конфигурацию
    console.log(config);
  });
```

### Проверка здоровья сервиса:
```bash
curl http://localhost:8000/health
```

## Деплой в Azure Web App

### 1. Создайте Web App в Azure Portal
### 2. Настройте Application Settings:
- `AZURE_SPEECH_KEY`: ваш ключ Azure Speech
- `AZURE_SPEECH_REGION`: регион Azure Speech
- `AZURE_OPENAI_KEY`: ваш ключ Azure OpenAI
- `AZURE_OPENAI_ENDPOINT`: endpoint Azure OpenAI
- `AZURE_OPENAI_DEPLOYMENT`: имя развертывания модели
- `ENVIRONMENT`: production

### 3. Деплойте код через:
- GitHub Actions
- Azure DevOps
- ZIP deploy
- Git deployment

### 4. Используйте startup.sh как команду запуска в Azure Web App

## Безопасность

- ✅ Все ключи загружаются из переменных окружения
- ✅ Никакие чувствительные данные не логируются
- ✅ CORS настроен для безопасного доступа из браузера
- ✅ Валидация входных и выходных данных
- ✅ Правильная обработка ошибок

## Мониторинг

### Endpoints для мониторинга:
- `GET /health` - проверка здоровья сервиса
- `GET /` - информация о сервисе

### Логирование:
- Structured logging с различными уровнями
- Безопасное логирование без раскрытия ключей
- Метрики загрузки конфигурации

## Тестирование

### Локальное тестирование:
```bash
# Запустите сервер
python main.py

# Тестируйте endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/config
```

### Тестирование в браузере:
- Откройте http://localhost:8000/docs для Swagger UI
- Откройте http://localhost:8000/redoc для ReDoc

## Troubleshooting

### Проблема: "uvicorn is not installed"
**Решение:** `pip install uvicorn`

### Проблема: "Failed to load configuration"
**Решение:** Проверьте переменные окружения

### Проблема: CORS ошибки
**Решение:** Обновите CORS_ORIGINS в config.py для production

### Проблема: Порт уже используется
**Решение:** Установите переменную `PORT` на другое значение
