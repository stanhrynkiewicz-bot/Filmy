# Profesjonalna Aplikacja do Dubbingu Filmów

Kompleksowa aplikacja do dubbingu filmów angielskich na język polski, specjalnie zaprojektowana dla filmów o tradingu. Wykorzystuje najnowsze technologie AI z obsługą CUDA.

## Funkcje

### Główne Możliwości
- 🎤 **Transkrypcja** - Lokalne przetwarzanie audio z Whisper + CUDA
- 🌐 **Tłumaczenie** - Automatyczne tłumaczenie angielski → polski
- 🗣️ **Lektor TTS** - Generowanie polskiego głosu lektora
- 🎬 **Przetwarzanie Wideo** - Inteligentne dopasowanie segmentów

### Zaawansowane Funkcje
- ⚡ **Akceleracja GPU** - Pełne wsparcie CUDA dla szybkiego przetwarzania
- 📝 **Edytowalny Słownik** - Niestandardowe tłumaczenia terminów tradingowych
- ✏️ **Edycja Tłumaczeń** - Możliwość poprawy tłumaczeń przed generowaniem lektora
- ⏱️ **Dopasowanie Tempa** - Automatyczne dopasowanie długości wideo do audio
- 🔑 **Klatki Kluczowe** - Dodawanie klatek kluczowych na granicach segmentów
- 🔇 **Usuwanie Ciszy** - Inteligentne usuwanie krótkich przerw (< 0.4s)
- 💾 **Zapisywanie Ustawień** - Trwałe przechowywanie konfiguracji
- 🖥️ **GUI Windows-style** - Intuicyjny interfejs w stylu Windows

## Wymagania Systemowe

### Sprzęt
- **GPU NVIDIA** z obsługą CUDA (zalecane dla optymalnej wydajności)
- **RAM**: Min. 8GB (zalecane 16GB+)
- **Miejsce na dysku**: Min. 10GB wolnego miejsca

### Oprogramowanie
- **Python** 3.8 lub nowszy
- **CUDA Toolkit** 11.8+ (dla obsługi GPU)
- **FFmpeg** (do przetwarzania wideo)

## Instalacja

### 1. Przygotowanie Środowiska

#### Windows
```bash
# Zainstaluj Python 3.8+
# Pobierz z https://www.python.org/downloads/

# Zainstaluj CUDA Toolkit
# Pobierz z https://developer.nvidia.com/cuda-downloads

# Zainstaluj FFmpeg
# Pobierz z https://ffmpeg.org/download.html
# Dodaj do PATH
```

#### Linux
```bash
# Zainstaluj Python i pip
sudo apt update
sudo apt install python3 python3-pip

# Zainstaluj CUDA (przykład dla Ubuntu)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install cuda

# Zainstaluj FFmpeg
sudo apt install ffmpeg
```

### 2. Instalacja Zależności

```bash
# Sklonuj repozytorium
git clone https://github.com/stanhrynkiewicz-bot/Filmy.git
cd Filmy

# Utwórz środowisko wirtualne (zalecane)
python -m venv venv

# Aktywuj środowisko
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Zainstaluj PyTorch z CUDA (dostosuj wersję CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. Weryfikacja Instalacji

```bash
# Sprawdź dostępność CUDA
python -c "import torch; print(f'CUDA dostępna: {torch.cuda.is_available()}')"
```

## Użycie

### Uruchomienie Aplikacji

```bash
# Upewnij się, że środowisko wirtualne jest aktywowane
python dubbing_app.py
```

### Podstawowy Workflow

1. **Wybierz Film**
   - Kliknij "Wybierz Film"
   - Wybierz plik wideo (mp4, avi, mkv, mov)

2. **Podgląd Transkrypcji** (Opcjonalnie)
   - Kliknij "Podgląd Transkrypcji"
   - Zobacz wykryte segmenty dialogu

3. **Edytuj Słownik** (Opcjonalnie)
   - Kliknij "Edytuj Słownik"
   - Dodaj specjalistyczne terminy tradingowe
   - Przykład: "candlestick" → "świeca"

4. **Edytuj Tłumaczenia** (Opcjonalnie)
   - Kliknij "Edytuj Tłumaczenia"
   - Popraw automatyczne tłumaczenia
   - Zapisz zmiany

5. **Rozpocznij Dubbing**
   - Kliknij "Rozpocznij Dubbing"
   - Poczekaj na zakończenie procesu
   - Gotowy film zostanie zapisany w katalogu `output/`

### Struktura Katalogów

```
Filmy/
├── dubbing_app.py          # Główny plik aplikacji
├── requirements.txt        # Zależności Python
├── config.yaml            # Konfiguracja (tworzona automatycznie)
├── custom_dictionary.json # Słownik niestandardowy
├── src/                   # Kod źródłowy
│   ├── core/             # Silnik dubbingu
│   ├── gui/              # Interfejs graficzny
│   └── utils/            # Narzędzia pomocnicze
├── output/               # Pliki wyjściowe
├── temp_segments/        # Pliki tymczasowe
└── models/               # Modele ML (pobierane automatycznie)
```

## Konfiguracja

### Szybkie Ustawienia (w aplikacji)
- **Model Whisper**: tiny/base/small/medium/large
- **CUDA**: Włącz/wyłącz akcelerację GPU
- **Dopasowanie Tempa**: Automatyczne dopasowanie długości wideo
- **Klatki Kluczowe**: Dodawanie klatek na granicach segmentów

### Ustawienia Zaawansowane
Dostępne przez zakładkę "Ustawienia" → "Otwórz Ustawienia Zaawansowane":

- **Whisper**: Model, urządzenie, język
- **Tłumaczenie**: Języki, serwis
- **TTS**: Model głosu polskiego
- **Wideo**: Progi ciszy, długość segmentów
- **Audio**: Sample rate, progi
- **Ścieżki**: Katalogi robocze

### Plik Konfiguracyjny (config.yaml)
```yaml
whisper:
  model_size: "medium"
  device: "cuda"
  language: "en"

translation:
  source_lang: "en"
  target_lang: "pl"

tts:
  model_name: "tts_models/pl/mai_female/vits"

video:
  silence_threshold: 0.4
  tempo_adjustment_enabled: true
  add_keyframes: true
```

## Słownik Niestandardowy

Aplikacja zawiera wbudowany słownik terminów tradingowych. Można go rozszerzyć:

```json
{
  "trading_terms": {
    "trading": "trading",
    "forex": "forex",
    "bullish": "zwyżkujący",
    "bearish": "spadkowy",
    "candlestick": "świeca",
    "resistance": "opór",
    "support": "wsparcie"
  }
}
```

## Algorytm Przetwarzania

### 1. Ekstrakcja Audio
- Wyodrębnienie ścieżki audio z wideo

### 2. Transkrypcja (Whisper + CUDA)
- Wykrywanie segmentów mowy
- Transkrypcja do tekstu angielskiego
- Znaczniki czasowe dla każdego segmentu

### 3. Optymalizacja Segmentów
- Łączenie zbyt krótkich segmentów (< 1s)
- Dzielenie zbyt długich segmentów (> 30s)
- Usuwanie ciszy < 0.4s

### 4. Tłumaczenie
- Zastosowanie słownika niestandardowego
- Automatyczne tłumaczenie Google
- Możliwość edycji przed TTS

### 5. Generowanie Lektora (TTS)
- Polski głos syntetyczny
- Wysokiej jakości audio

### 6. Przetwarzanie Wideo

#### Dla krótszych segmentów (wideo < audio):
- Dodanie klatek kluczowych na początku/końcu
- Dopasowanie tempa wideo do długości audio
- Zachowanie synchronizacji

#### Dla dłuższych segmentów (wideo > audio):
- Lektor na początku segmentu
- Wypełnienie reszty ciszą
- Brak zmiany tempa

### 7. Finalizacja
- Usunięcie oryginalnej ścieżki audio
- Dodanie nowej ścieżki lektora
- Eksport do MP4

## Rozwiązywanie Problemów

### CUDA nie jest dostępna
```bash
# Sprawdź instalację CUDA
nvidia-smi

# Reinstaluj PyTorch z CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Błąd braku FFmpeg
```bash
# Windows: Pobierz i dodaj do PATH
# Linux:
sudo apt install ffmpeg
```

### Błędy pamięci GPU
- Zmniejsz rozmiar modelu Whisper (tiny/base/small)
- Użyj CPU zamiast CUDA (wolniejsze)

### Problemy z modelami TTS
- Modele są pobierane automatycznie przy pierwszym użyciu
- Upewnij się, że masz połączenie z internetem
- Sprawdź katalog `models/`

## Wydajność

### Szacowany czas przetwarzania (GPU NVIDIA RTX 3060):
- **1 minuta wideo**: ~2-3 minuty
- **10 minut wideo**: ~15-25 minut
- **30 minut wideo**: ~45-75 minut

### Optymalizacja:
- **Mniejszy model Whisper** = szybsze przetwarzanie, niższa jakość
- **GPU CUDA** = 5-10x szybciej niż CPU
- **Więcej VRAM** = większe modele, lepsza jakość

## Licencja

Ten projekt wykorzystuje następujące biblioteki open-source:
- Whisper (OpenAI)
- TTS (Coqui)
- MoviePy
- PyQt5

## Autor

Stworzone dla potrzeb nauki tradingu z filmów anglojęzycznych.

## Wsparcie

W przypadku problemów:
1. Sprawdź sekcję "Rozwiązywanie Problemów"
2. Przejrzyj logi w aplikacji
3. Otwórz issue na GitHub

---

**Uwaga**: Pierwszego uruchomienie może potrwać dłużej, ponieważ modele (Whisper, TTS) są pobierane automatycznie.