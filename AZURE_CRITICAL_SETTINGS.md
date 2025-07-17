# КРИТИЧЕСКИЕ НАСТРОЙКИ AZURE APP SERVICE

## Проблема: Exit Code 127 означает "команда не найдена"

### 1. Проверьте настройки в Azure Portal:

**Configuration → General Settings:**
- **Stack:** Python
- **Major version:** 3.11
- **Minor version:** 3.11 (latest)
- **Startup Command:** `python diagnostic.py`

### 2. Убедитесь в правильности развертывания:

**Deployment Center:**
- **Source:** External Git или Local Git
- **Branch:** main
- **Build Provider:** App Service build service

### 3. Проверьте Application Settings:

**Configuration → Application Settings:**
- `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
- `ENABLE_ORYX_BUILD` = `true`
- `POST_BUILD_SCRIPT_PATH` = (пусто)

### 4. Если все еще не работает:

**Попробуйте альтернативные startup commands:**
```bash
# Вариант 1:
python3 diagnostic.py

# Вариант 2:
/opt/python/3.11.8/bin/python diagnostic.py

# Вариант 3:
python -u diagnostic.py

# Вариант 4:
/tmp/*/diagnostic.py
```

### 5. Проверьте логи:

**В Azure Portal → Monitoring → Log stream**

### 6. Сброс настроек:

Если ничего не помогает:
1. Остановите App Service
2. Удалите все файлы через Kudu Console
3. Переразверните заново
4. Установите startup command: `python diagnostic.py`

### 7. Альтернативный подход:

Создайте новый App Service с теми же настройками и проверьте, работает ли он.

## Ожидаемый результат:

diagnostic.py должен вывести полную информацию о среде в логи, что поможет понять, что именно не работает.

## Если и diagnostic.py не работает:

Проблема в базовой конфигурации Azure App Service или Python runtime.
