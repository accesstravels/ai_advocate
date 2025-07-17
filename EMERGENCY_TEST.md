🔧 ЭКСТРЕННЫЙ ТЕСТ ДЛЯ РЕШЕНИЯ EXIT CODE 127

## Текущее состояние:
- main.py = простой HTTP сервер (без зависимостей)
- requirements.txt = пустой файл

## Цель:
Проверить, что проблема НЕ в Python или зависимостях, а в конфигурации Azure App Service.

## Шаги:

### 1. Деплой через VS Code:
1. Убедитесь что файлы сохранены
2. В VS Code Azure панели найдите App Service
3. Правый клик → "Deploy to Web App"
4. Выберите эту папку

### 2. Настройка в Azure Portal:
Перейдите в Configuration > General Settings:
- **Startup Command:** `python main.py`
- **Stack:** Python 3.11
- **Always On:** Off (для тестирования)

### 3. Проверка:
После деплоя проверьте:
- Логи в VS Code (Start Streaming Logs)
- Эндпоинты:
  - `https://aiadvokatweb-fpd4hxd0beephzhx.eastus2-01.azurewebsites.net/`
  - `https://aiadvokatweb-fpd4hxd0beephzhx.eastus2-01.azurewebsites.net/health`

### 4. Если это работает:
Значит проблема была в зависимостях или конфигурации FastAPI.

### 5. Если НЕ работает:
Проблема в настройках Azure App Service или Python runtime.

## Восстановление FastAPI версии:
```cmd
copy "main_fastapi.py" "main.py"
copy "requirements_minimal.txt" "requirements.txt"
```

## Ожидаемый результат:
Простой HTTP сервер должен запуститься и отвечать JSON с информацией о системе.

Этот тест поможет точно определить источник проблемы!
