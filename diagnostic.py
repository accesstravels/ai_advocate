#!/usr/bin/env python3
"""
Простейший тест для диагностики Azure App Service
"""
import os
import sys
import time

print("=" * 50)
print("ДИАГНОСТИКА AZURE APP SERVICE")
print("=" * 50)

print(f"Python версия: {sys.version}")
print(f"Python путь: {sys.executable}")
print(f"Рабочая директория: {os.getcwd()}")
print(f"Аргументы: {sys.argv}")

print("\nПеременные окружения:")
for key, value in sorted(os.environ.items()):
    if key.startswith(('AZURE_', 'WEBSITE_', 'PORT', 'HOST', 'PYTHON')):
        print(f"  {key}={value}")

print("\nСодержимое директории:")
try:
    for item in os.listdir('.'):
        print(f"  {item}")
except Exception as e:
    print(f"  Ошибка: {e}")

print("\nТест сети:")
import socket
try:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f"  Hostname: {hostname}")
    print(f"  IP: {ip}")
except Exception as e:
    print(f"  Ошибка: {e}")

print("\nТест времени:")
print(f"  Текущее время: {time.strftime('%Y-%m-%d %H:%M:%S')}")

print("\nЗапуск простого HTTP сервера...")
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello from Azure App Service!')
    
    port = int(os.environ.get("PORT", 8000))
    print(f"Сервер запускается на порту {port}")
    server = HTTPServer(('0.0.0.0', port), TestHandler)
    server.serve_forever()
    
except Exception as e:
    print(f"Ошибка запуска сервера: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
