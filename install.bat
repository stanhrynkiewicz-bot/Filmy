@echo off
REM Skrypt instalacyjny dla Windows

echo ==========================================
echo Instalacja Aplikacji do Dubbingu Filmow
echo ==========================================
echo.

REM Sprawdz Pythona
echo Sprawdzanie Pythona...
python --version >nul 2>&1
if errorlevel 1 (
    echo BLAD: Python nie jest zainstalowany!
    echo Zainstaluj Python 3.8 lub nowszy z https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM Sprawdz FFmpeg
echo Sprawdzanie FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo OSTRZEZENIE: FFmpeg nie jest zainstalowany!
    echo FFmpeg jest wymagany do przetwarzania wideo.
    echo.
    echo Pobierz z: https://ffmpeg.org/download.html
    echo Dodaj do PATH i uruchom ponownie
    echo.
    pause
)

REM Sprawdz CUDA
echo Sprawdzanie CUDA...
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo CUDA niedostepna - bedzie uzywany CPU ^(wolniejsze^)
) else (
    echo CUDA dostepna
    nvidia-smi --query-gpu=name --format=csv,noheader
)
echo.

REM Utworz srodowisko wirtualne
echo Tworzenie srodowiska wirtualnego...
if not exist "venv" (
    python -m venv venv
    echo Srodowisko utworzone
) else (
    echo Srodowisko juz istnieje
)
echo.

REM Aktywuj srodowisko
echo Aktywacja srodowiska...
call venv\Scripts\activate.bat

REM Aktualizuj pip
echo Aktualizacja pip...
python -m pip install --upgrade pip

REM Instaluj zaleznosci
echo.
echo Instalacja zaleznosci...
echo To moze potrawac kilka minut...
pip install -r requirements.txt

REM Instaluj PyTorch z CUDA
echo.
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo Instalacja PyTorch ^(CPU only^)...
    pip install torch torchvision torchaudio
) else (
    echo Instalacja PyTorch z obsluga CUDA...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
)

REM Utworz katalogi
echo.
echo Tworzenie katalogow...
if not exist "output" mkdir output
if not exist "temp_segments" mkdir temp_segments
if not exist "cache" mkdir cache
if not exist "models" mkdir models

REM Skopiuj template config
if not exist "config.yaml" (
    copy config.yaml.template config.yaml
    echo Utworzono config.yaml
)

echo.
echo ==========================================
echo Instalacja zakonczona!
echo ==========================================
echo.
echo Aby uruchomić aplikacje:
echo   1. Aktywuj srodowisko: venv\Scripts\activate.bat
echo   2. Uruchom aplikacje: python dubbing_app.py
echo.
echo Wiecej informacji w README.md
echo.
pause
