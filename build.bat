echo off
cls
start /min cmd /c "ngrok http 8000"
python src/main.py
