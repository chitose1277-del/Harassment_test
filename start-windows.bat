@echo off
rem index.html を直接開くと assets を読み込めないため、簡易サーバー経由で開きます
cd /d "%~dp0"
start "" http://localhost:8000
python -m http.server 8000
