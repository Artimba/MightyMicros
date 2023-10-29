@echo off
set "venv_dir=mighty"

if not exist "%venv_dir%" (
    echo Creating virtual environment...
    python -m venv %venv_dir%
) else (
    echo Virtual environment exists.
)

echo Activating virtual environment...
call .\%venv_dir%\Scripts\Activate

if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found.
)
