echo off
cls
start /min cmd /c "ngrok http 8000"
start /min cmd /c "python server.py"
start chrome