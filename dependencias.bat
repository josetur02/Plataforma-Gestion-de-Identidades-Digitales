@echo off
echo =======================================================
echo   Instalando dependencias de la Plataforma PKI - TFG
echo =======================================================
echo.

:: Comprueba si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Por favor, instala Python 3 desde python.org
    pause
    exit /b
)

:: Actualiza pip (el instalador) e instala lo que hay en requirements.txt
echo Actualizando gestor de paquetes...
python -m pip install --upgrade pip >nul

echo.
echo Instalando librerias necesarias...
pip install -r requirements.txt

echo.
echo =======================================================
echo   ¡Todo listo! Instalacion completada con exito.
echo =======================================================
pause