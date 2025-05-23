@echo off
echo ========================================================================
echo  Script de Inicio para el Dashboard de Analisis y Forecasting ARIMA
echo ========================================================================
echo.

REM -- INSTRUCCIONES PARA EL USUARIO (Importante para GitHub) --
echo NOTA IMPORTANTE PARA EL USUARIO:
echo 1. Asegurate de tener un entorno de Python (conda o venv) activado
echo    con Python 3.x instalado.
echo 2. Este script intentara instalar las dependencias de 'requirements.txt'.
echo 3. Deberas tener tu propio archivo de credenciales JSON de Google Cloud.
echo    Este script te pedira la ruta a ese archivo.
echo 4. Deberás subir a tu propia cuenta de Google Cloud la base de datos online_retail_II_clean.csv. 
echo.
pause
echo.

REM Ir a carpeta del proyecto (asumiendo que el .bat está en la raíz del proyecto)
echo Cambiando al directorio del script (%~dp0)...
cd /D "%~dp0"
if errorlevel 1 (
    echo ERROR: No se pudo cambiar al directorio del script.
    pause
    exit /b 1
)





REM Verificar e instalar requerimientos
echo Verificando e instalando requerimientos desde requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ADVERTENCIA: Hubo un problema al instalar/verificar los paquetes de requirements.txt.
    echo Por favor, revisa los mensajes de error de pip e intenta instalar
    echo manualmente si es necesario con: pip install -r requirements.txt
    pause
    exit /b 1
) else (
    echo Requerimientos instalados/verificados correctamente.
)
echo.

REM Solicitar la ruta al archivo de credenciales y el ID del proyecto
echo --- Configuracion de Google Cloud ---
set /p KEY_PATH_INPUT="Por favor, ingresa la ruta COMPLETA a tu archivo JSON de credenciales de Google Cloud: "
set /p PROJECT_ID_INPUT="Por favor, ingresa tu Project ID de Google Cloud: "

if not exist "%KEY_PATH_INPUT%" (
    echo ERROR: El archivo de credenciales especificado no existe: %KEY_PATH_INPUT%
    pause
    exit /b 1
)
if "%PROJECT_ID_INPUT%"=="" (
    echo ERROR: El Project ID no puede estar vacio.
    pause
    exit /b 1
)
echo.

REM Ejecutar app
echo Ejecutando la aplicacion Dash...
python main.py --key_path "%KEY_PATH_INPUT%" --project_id "%PROJECT_ID_INPUT%"
if errorlevel 1 (
    echo ERROR: Hubo un problema al ejecutar main.py.
    pause
    exit /b 1
)

echo La aplicacion Dash deberia estar ejecutandose.
echo Si no se abrio automaticamente, abre tu navegador en http://127.0.0.1:8050/
pause
