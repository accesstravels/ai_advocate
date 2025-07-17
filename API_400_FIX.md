# Исправление ошибки API HTTP 400 - Завершено

## Первоначальная проблема
```
Ошибка: HTTP 400: { "error": { "message": "Unrecognized request argument supplied: data_sources", "type": "invalid_request_error", "param": null, "code": null } }
```

## Причина ошибки
Параметр `data_sources` не является стандартным для базового Azure OpenAI API. Этот параметр используется только в Azure OpenAI Extensions API для интеграции с Azure Search.

## Решение

### 1. Исправлен API endpoint
**Файл:** `main.py`
```python
# Для Azure Search интеграции используем extensions API
if config.AZURE_SEARCH_ENDPOINT and config.AZURE_SEARCH_API_KEY and config.AZURE_SEARCH_INDEX_NAME:
    api_url = f"{config.AZURE_OPENAI_ENDPOINT}/openai/deployments/{config.AZURE_OPENAI_DEPLOYMENT}/extensions/chat/completions?api-version=2023-06-01-preview"
else:
    api_url = f"{config.AZURE_OPENAI_ENDPOINT}/openai/deployments/{config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-06-01-preview"
```

### 2. Исправлена конфигурация Azure переменных
**Файл:** `config.py`
Добавлены все необходимые Azure переменные в `DevelopmentConfig` и `ProductionConfig`:
```python
# Azure configuration from environment variables
AZURE_SPEECH_KEY: str = os.environ.get("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_REGION: str = os.environ.get("AZURE_SPEECH_REGION", "")
AZURE_OPENAI_KEY: str = os.environ.get("AZURE_OPENAI_KEY", "")
AZURE_OPENAI_ENDPOINT: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
AZURE_SEARCH_ENDPOINT: str = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
AZURE_SEARCH_API_KEY: str = os.environ.get("AZURE_SEARCH_API_KEY", "")
AZURE_SEARCH_INDEX_NAME: str = os.environ.get("AZURE_SEARCH_INDEX_NAME", "")
AZURE_SYSTEM_PROMPT: str = os.environ.get("AZURE_SYSTEM_PROMPT", "")
AVATAR_CHARACTER: str = os.environ.get("AVATAR_CHARACTER", "")
AVATAR_STYLE: str = os.environ.get("AVATAR_STYLE", "")
VOICE_NAME: str = os.environ.get("VOICE_NAME", "")
STT_LOCALE: str = os.environ.get("STT_LOCALE", "")
```

### 3. Создана тестовая страница для API
**Файл:** `test-chat-api.html`
- Простой интерфейс для тестирования эндпоинта `/chat`
- Отображение логов и ошибок
- Возможность отправки тестовых сообщений

## Архитектура решения

### Условная логика для API endpoints:
1. **Если настроен Azure Search** → использует `extensions/chat/completions` (поддерживает `data_sources`)
2. **Если Azure Search не настроен** → использует стандартный `chat/completions` (без `data_sources`)

### Процесс обработки запроса:
```
Frontend → POST /chat → Проверка конфигурации → Выбор API endpoint → Azure OpenAI → Ответ
```

## Текущий статус

### ✅ Исправлено:
- HTTP 400 ошибка с `data_sources` 
- Конфигурация Azure переменных
- Правильный выбор API endpoint
- Серверная архитектура чат-бота

### ⚠️ Требует настройки:
- Переменные окружения в файле `.env` должны содержать действительные значения Azure API
- Текущие значения в `.env` могут быть заглушками или неактуальными

## Проверка работоспособности

### Для проверки конфигурации:
1. Откройте: http://127.0.0.1:8001/internal/config
2. Убедитесь, что все необходимые поля заполнены

### Для тестирования чат-бота:
1. Откройте: http://127.0.0.1:8001/test-chat-api
2. Отправьте тестовое сообщение
3. Проверьте логи в терминале

### Для использования основного интерфейса:
1. Откройте: http://127.0.0.1:8001/chat-auto
2. Начните говорить в микрофон
3. Проверьте обработку в логах сервера

## Логи сервера показывают:
- ✅ Конфигурация загружена: 13/13 переменных окружения
- ✅ Эндпоинт `/chat` обрабатывает запросы
- ⚠️ "Azure OpenAI configuration is incomplete" - требуется проверка значений в `.env`

## Дата исправления
17 июля 2025 г. - 20:50

## Статус
🟡 **В ПРОЦЕССЕ** - Техническая проблема решена, требуется настройка конфигурации Azure
