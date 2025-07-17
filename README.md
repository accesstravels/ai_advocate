# Azure AI Avatar Configuration Service

FastAPI-приложение для предоставления безопасной конфигурации Azure AI Avatar приложений.

## Особенности

- ✅ Безопасная загрузка конфигурации из переменных окружения
- ✅ REST API endpoint для получения конфигурации
- ✅ CORS поддержка для браузерных приложений
- ✅ Готовность к деплою в Azure Web App
- ✅ Валидация данных с помощью Pydantic
- ✅ Логирование без раскрытия чувствительных данных
- ✅ Health check endpoints

## Быстрый старт

### Локальная разработка

1. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

2. **Настройка переменных окружения:**
```bash
# Скопируйте пример файла
copy .env.example .env

# Отредактируйте .env файл, добавив ваши Azure ключи
```

3. **Запуск приложения:**
```bash
python main.py
```

Или с помощью uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Деплой в Azure Web App

1. **Создайте Web App в Azure Portal**
2. **Настройте переменные окружения** в Configuration → Application Settings
3. **Деплойте код** через GitHub Actions, Azure DevOps или ZIP deploy

## API Endpoints

### GET /config
Возвращает конфигурацию приложения из переменных окружения.

**Ответ:**
```json
{
  "azure_speech_key": "your-key",
  "azure_speech_region": "eastus2",
  "azure_openai_key": "your-key",
  "azure_openai_endpoint": "https://your-resource.openai.azure.com/",
  "azure_openai_deployment": "gpt-4o",
  "azure_system_prompt": "ваш системный промпт",
  "azure_search_endpoint": "https://your-search.search.windows.net",
  "azure_search_api_key": "your-search-key",
  "azure_search_index_name": "your-index",
  "avatar_character": "meg",
  "avatar_style": "formal",
  "voice_name": "ru-RU-DmitryNeural",
  "stt_locale": "ru-RU"
}
```

### GET /health
Health check endpoint для мониторинга.

### GET /
Информация о сервисе.

## Переменные окружения

| Переменная | Описание | Обязательная |
|------------|----------|-------------|
| `AZURE_SPEECH_KEY` | Ключ Azure Speech Service | Да |
| `AZURE_SPEECH_REGION` | Регион Azure Speech Service | Да |
| `AZURE_OPENAI_KEY` | Ключ Azure OpenAI Service | Да |
| `AZURE_OPENAI_ENDPOINT` | Endpoint Azure OpenAI Service | Да |
| `AZURE_OPENAI_DEPLOYMENT` | Имя деплоя модели | Да |
| `AZURE_SYSTEM_PROMPT` | Системный промпт для ИИ | Да |
| `AZURE_SEARCH_ENDPOINT` | Endpoint Azure Cognitive Search | Нет |
| `AZURE_SEARCH_API_KEY` | Ключ Azure Cognitive Search | Нет |
| `AZURE_SEARCH_INDEX_NAME` | Имя индекса поиска | Нет |
| `AVATAR_CHARACTER` | Персонаж аватара | Нет |
| `AVATAR_STYLE` | Стиль аватара | Нет |
| `VOICE_NAME` | Имя голоса для TTS | Нет |
| `STT_LOCALE` | Локаль для распознавания речи | Нет |
| `PORT` | Порт для запуска (по умолчанию 8000) | Нет |

## Интеграция с frontend

Обновите ваш `chat.html` для загрузки конфигурации из API:

```javascript
// Замените hardcoded значения на вызов API
fetch('/config')
  .then(response => response.json())
  .then(config => {
    document.getElementById("region").value = config.azure_speech_region;
    document.getElementById("APIKey").value = config.azure_speech_key;
    document.getElementById("azureOpenAIEndpoint").value = config.azure_openai_endpoint;
    // ... и т.д.
  });
```

## Безопасность

- 🔐 Все чувствительные данные загружаются из переменных окружения
- 🔐 API ключи никогда не логируются в консоль
- 🔐 CORS настроен для доступа из браузера
- 🔐 Валидация всех входных и выходных данных
- 🔐 Обработка ошибок без раскрытия внутренней информации

## Мониторинг

Приложение включает:
- Structured logging
- Health check endpoint
- Error handling с соответствующими HTTP статусами
- Метрики загрузки конфигурации

## Требования

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Python-dotenv

## Лицензия

MIT License

---

# Оригинальный Azure AI Avatar
Azure AI Avatar using Azure TTS, Azure OpenAI and AI Search RAG

# Watch the Video for Step by Step Configuration

[![Video Title](https://img.youtube.com/vi/rVG2Y8CWNb0/0.jpg)](https://www.youtube.com/watch?v=rVG2Y8CWNb0)
