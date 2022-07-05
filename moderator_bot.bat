@echo off

call %~dp0venvzelya\Scripts\activate

cd %~dp0

set TOKEN=721299835:AAExB9wUY4vCfXbPm_GaNRAvYE8zfamL1cI

py main.py

pause
