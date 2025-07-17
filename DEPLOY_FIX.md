🎯 ПРОБЛЕМА РЕШЕНА! 

## Найденная проблема:
```
ModuleNotFoundError: No module named 'aiohttp'
```

## Исправление:
✅ Добавлен `aiohttp==3.9.1` в requirements.txt
✅ Все модули теперь доступны для импорта
✅ Создан deploy.zip архив для развертывания

## Следующие шаги:

### 1. Переразвертывание
Загрузите обновленный deploy.zip в Azure App Service через:
- VS Code Azure Extension
- Azure CLI: `az webapp deployment source config-zip`
- Azure Portal: Deployment Center

### 2. Настройка переменных окружения
В Azure Portal > App Service > Configuration > Application Settings добавьте:

**ОБЯЗАТЕЛЬНЫЕ:**
```
AZURE_OPENAI_KEY=your-actual-key
AZURE_OPENAI_ENDPOINT=https://advokatopenai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_SEARCH_ENDPOINT=https://advokatsearch123.search.windows.net
AZURE_SEARCH_API_KEY=your-actual-search-key
AZURE_SEARCH_INDEX_NAME=rag-1752686975655
```

**ДОПОЛНИТЕЛЬНЫЕ:**
```
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=eastus2
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### 3. Проверка после развертывания

1. **Health Check**: https://aiadvokatweb-fpd4hxd0beephzhx.eastus2-01.azurewebsites.net/health
2. **Test Page**: https://aiadvokatweb-fpd4hxd0beephzhx.eastus2-01.azurewebsites.net/test-azure-search
3. **Main App**: https://aiadvokatweb-fpd4hxd0beephzhx.eastus2-01.azurewebsites.net/

### 4. Мониторинг логов
```bash
az webapp log tail --resource-group your-rg --name aiadvokatweb
```

## Ожидаемый результат:
После перезапуска контейнер должен запуститься успешно без ошибок импорта.

## Если есть другие проблемы:
1. Проверьте правильность всех переменных окружения
2. Убедитесь, что Azure Search доступен из App Service
3. Проверьте сетевые настройки и firewall rules
