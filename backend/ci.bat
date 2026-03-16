@echo off
setlocal
echo ========================================
echo   EJECUTANDO PIPELINE DE BACKEND
echo ========================================

echo [1/3] Activando entorno virtual...
if not exist .venv (
    echo [ERROR] No se encuentra la carpeta .venv. Ejecuta esto desde la carpeta backend.
    exit /b 1
)
call .venv\Scripts\activate

echo [2/3] Ejecutando Pytest...

python -m pytest tests/test_app.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Las pruebas unitarias fallaron.
    exit /b %errorlevel%
)

echo [3/3] Ejecutando Pylint...

python -m pylint app.py db.py --disable=C0114,C0116,C0103,R0914
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Pylint detecto problemas serios.
    exit /b %errorlevel%
)

echo.
echo ========================================
echo   BACKEND CI: EXITOSO
echo ========================================
pause