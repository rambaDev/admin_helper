@echo off

call %~dp0venvzelya\Scripts\activate

cd %~dp0

set TOKEN=ВСТАВИТЬ ТОКЕН БОТА

py main.py

pause
