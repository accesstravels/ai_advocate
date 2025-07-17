# Azure App Service Configuration for VS Code Deployment

## Шаги для деплоя через VS Code:

### 1. Подготовка файлов
Убедитесь, что у вас есть эти файлы в корне проекта:
- ✅ main.py (или main_debug.py для отладки)
- ✅ requirements.txt
- ✅ config.py
- ✅ .env (не деплоится, только для локальной разработки)

### 2. Правильная последовательность деплоя:

1. **Откройте VS Code**
2. **Установите Azure App Service Extension** (если еще не установлено)
3. **Войдите в Azure** через Command Palette (Ctrl+Shift+P) → "Azure: Sign In"
4. **Откройте Azure панель** (иконка Azure в левой панели)
5. **Найдите свой App Service** в списке
6. **Правый клик на App Service** → "Deploy to Web App"
7. **Выберите папку проекта** (c:\AI-Advokat\Azure-Ai-Avatar)

### 3. Рекомендуемый workflow:

#### Первый деплой (отладка):
1. Переименуйте main.py в main_backup.py
2. Переименуйте main_debug.py в main.py
3. Деплойте через VS Code
4. Проверьте что приложение запускается

#### После успешного запуска:
1. Верните main_backup.py в main.py
2. Задеплойте снова

### 4. Настройки после деплоя:
Перейдите в Azure Portal > App Service > Configuration:

**Application Settings:**
```
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://advokatopenai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_SEARCH_ENDPOINT=https://advokatsearch123.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key
AZURE_SEARCH_INDEX_NAME=rag-1752686975655
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

**General Settings:**
- Stack: Python 3.11
- Startup Command: (оставьте пустым, будет использоваться main.py автоматически)

### 5. Проверка логов после деплоя:
В VS Code:
1. Правый клик на App Service → "Start Streaming Logs"
2. Или в Azure Portal → Log Stream

### 6. Если проблемы:
1. Проверьте Output в VS Code (View → Output → Azure App Service)
2. Убедитесь что все файлы загружены
3. Проверьте что Python 3.11 выбран в Azure Portal

### 7. Структура файлов для VS Code:
```
c:\AI-Advokat\Azure-Ai-Avatar\
├── main.py (или main_debug.py)
├── requirements.txt
├── config.py
├── chat.html
├── css/
├── js/
├── image/
└── другие файлы...
```

VS Code автоматически создаст .zip и загрузит его в Azure App Service.
