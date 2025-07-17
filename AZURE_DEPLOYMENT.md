# Azure App Service Deployment Guide

## 📋 Пошаговая инструкция для развертывания

### 1. Подготовка файлов
Убедитесь, что у вас есть все файлы:
- ✅ `main.py` - основное приложение
- ✅ `requirements.txt` - зависимости Python
- ✅ `startup.sh` - скрипт запуска
- ✅ `web.config` - конфигурация IIS
- ✅ `config.py` - конфигурация приложения

### 2. Настройка переменных окружения в Azure App Service

Перейдите в Azure Portal > App Service > Configuration > Application Settings и добавьте:

#### Azure OpenAI
```
AZURE_OPENAI_KEY=your-openai-key
AZURE_OPENAI_ENDPOINT=https://advokatopenai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-10-21
```

#### Azure Search
```
AZURE_SEARCH_ENDPOINT=https://advokatsearch123.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key
AZURE_SEARCH_INDEX_NAME=rag-1752686975655
```

#### Azure Speech Service
```
AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=eastus2
```

#### Server Configuration
```
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### 3. Развертывание

#### Вариант А: Через Azure CLI
```bash
# Создание приложения
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name aiadvokatweb --runtime "PYTHON|3.11"

# Развертывание кода
az webapp deployment source config-zip --resource-group myResourceGroup --name aiadvokatweb --src deploy.zip
```

#### Вариант Б: Через VS Code
1. Установите расширение Azure App Service
2. Нажмите правой кнопкой на папку проекта
3. Выберите "Deploy to Web App"

### 4. Проверка развертывания

#### Проверьте логи:
```bash
az webapp log tail --resource-group myResourceGroup --name aiadvokatweb
```

#### Тестовые эндпоинты:
- `https://aiadvokatweb.azurewebsites.net/health` - проверка здоровья
- `https://aiadvokatweb.azurewebsites.net/` - главная страница
- `https://aiadvokatweb.azurewebsites.net/test-azure-search` - тест Azure Search

### 5. Решение проблем

#### Если контейнер не запускается:
1. Проверьте все переменные окружения
2. Убедитесь, что `requirements.txt` содержит все зависимости
3. Проверьте логи: `az webapp log tail`

#### Если Azure Search не работает:
1. Проверьте `AZURE_SEARCH_API_KEY` и `AZURE_SEARCH_ENDPOINT`
2. Убедитесь, что индекс `rag-1752686975655` существует
3. Проверьте, что IP адрес App Service добавлен в правила брандмауэра Azure Search

### 6. Мониторинг

#### Application Insights
Добавьте переменную окружения:
```
APPLICATIONINSIGHTS_CONNECTION_STRING=your-connection-string
```

#### Логирование
Включите логирование в Azure Portal:
Configuration > General Settings > Logging > Application Logging = On

### 7. Масштабирование

#### Для высокой нагрузки:
1. Измените App Service Plan на Standard или выше
2. Включите автомасштабирование
3. Настройте CDN для статических файлов

## 🔍 Диагностика проблем

### Частые ошибки:

1. **Container terminated** - проверьте переменные окружения
2. **Module not found** - проверьте `requirements.txt`
3. **Azure Search timeout** - проверьте сетевые настройки
4. **403 Forbidden** - проверьте API ключи

### Команды для диагностики:
```bash
# Проверка статуса приложения
az webapp show --resource-group myResourceGroup --name aiadvokatweb --query state

# Просмотр логов
az webapp log tail --resource-group myResourceGroup --name aiadvokatweb

# Перезапуск приложения
az webapp restart --resource-group myResourceGroup --name aiadvokatweb
```
