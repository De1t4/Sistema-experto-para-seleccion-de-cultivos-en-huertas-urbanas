@echo off
title Selector de cultivos - huerta AMBA
cd /d "%~dp0"
echo.
echo Levantando el servidor local...
echo En unos segundos se abre solo el navegador con la app.
echo Para apagar: cerra esta ventana (o apreta Ctrl+C aca adentro).
echo.
".venv\Scripts\streamlit.exe" run app.py
echo.
echo El servidor se detuvo.
pause
