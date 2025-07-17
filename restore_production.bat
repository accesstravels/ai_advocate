@echo off
echo Восстановление продакшн версии...

echo Восстанавливаем main.py...
copy "main_production.py" "main.py"

echo Восстанавливаем requirements.txt...
copy "requirements_production.txt" "requirements.txt"

echo Готово! Теперь можно деплоить продакшн версию.
pause
