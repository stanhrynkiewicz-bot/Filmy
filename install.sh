#!/bin/bash
# Skrypt instalacyjny dla Linux/Mac

echo "=========================================="
echo "Instalacja Aplikacji do Dubbingu Filmów"
echo "=========================================="
echo ""

# Sprawdź Pythona
echo "Sprawdzanie Pythona..."
if ! command -v python3 &> /dev/null; then
    echo "BŁĄD: Python 3 nie jest zainstalowany!"
    echo "Zainstaluj Python 3.8 lub nowszy i uruchom ponownie."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Znaleziono Python $PYTHON_VERSION"
echo ""

# Sprawdź FFmpeg
echo "Sprawdzanie FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "OSTRZEŻENIE: FFmpeg nie jest zainstalowany!"
    echo "FFmpeg jest wymagany do przetwarzania wideo."
    echo ""
    echo "Zainstaluj FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Mac: brew install ffmpeg"
    echo ""
    read -p "Kontynuować mimo to? (t/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Tt]$ ]]; then
        exit 1
    fi
else
    echo "FFmpeg zainstalowany ✓"
fi
echo ""

# Sprawdź CUDA (opcjonalnie)
echo "Sprawdzanie CUDA..."
if command -v nvidia-smi &> /dev/null; then
    echo "CUDA dostępna ✓"
    nvidia-smi --query-gpu=name --format=csv,noheader
else
    echo "CUDA niedostępna - będzie używany CPU (wolniejsze)"
fi
echo ""

# Utwórz środowisko wirtualne
echo "Tworzenie środowiska wirtualnego..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Środowisko utworzone ✓"
else
    echo "Środowisko już istnieje ✓"
fi
echo ""

# Aktywuj środowisko
echo "Aktywacja środowiska..."
source venv/bin/activate

# Aktualizuj pip
echo "Aktualizacja pip..."
pip install --upgrade pip

# Instaluj zależności
echo ""
echo "Instalacja zależności..."
echo "To może potrwać kilka minut..."
pip install -r requirements.txt

# Instaluj PyTorch z CUDA (jeśli dostępne)
echo ""
if command -v nvidia-smi &> /dev/null; then
    echo "Instalacja PyTorch z obsługą CUDA..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "Instalacja PyTorch (CPU only)..."
    pip install torch torchvision torchaudio
fi

# Utwórz katalogi
echo ""
echo "Tworzenie katalogów..."
mkdir -p output temp_segments cache models

# Skopiuj template config
if [ ! -f "config.yaml" ]; then
    cp config.yaml.template config.yaml
    echo "Utworzono config.yaml ✓"
fi

echo ""
echo "=========================================="
echo "Instalacja zakończona!"
echo "=========================================="
echo ""
echo "Aby uruchomić aplikację:"
echo "  1. Aktywuj środowisko: source venv/bin/activate"
echo "  2. Uruchom aplikację: python dubbing_app.py"
echo ""
echo "Więcej informacji w README.md"
echo ""
