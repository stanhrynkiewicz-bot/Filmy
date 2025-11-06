# Changelog

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
i projekt stosuje się do [Semantic Versioning](https://semver.org/lang/pl/).

## [1.0.0] - 2024-11-03

### ✨ Dodano

#### Core Features
- Transkrypcja audio z lokalnym Whisper + wsparcie CUDA
- Automatyczne tłumaczenie angielski→polski przez Google Translate
- Generowanie polskiego lektora TTS (Coqui)
- Inteligentne przetwarzanie segmentów wideo:
  - Dopasowanie tempa wideo dla krótszych segmentów
  - Dodawanie klatek kluczowych na granicach segmentów
  - Wypełnienie ciszą dla dłuższych segmentów
- Usuwanie oryginalnej ścieżki audio
- Usuwanie fragmentów ciszy krótszych niż 0.4s

#### GUI (PyQt5)
- Główne okno aplikacji w stylu Windows
- Zakładki: Główna, Ustawienia
- Wybór plików wejściowych/wyjściowych
- Pasek postępu i logi w czasie rzeczywistym
- Edytor niestandardowego słownika terminów tradingowych
- Edytor tłumaczeń przed generowaniem TTS
- Dialog zaawansowanych ustawień
- Zapisywanie i wczytywanie konfiguracji

#### Moduły Core
- `dubbing_engine.py` - Główny orchestrator procesu dubbingu
- `transcription.py` - Wrapper dla Whisper z optymalizacją segmentów
- `translation.py` - Moduł tłumaczenia ze wsparciem słownika
- `tts.py` - Generator polskiego głosu
- `video_processor.py` - Kompletne przetwarzanie wideo/audio

#### Moduły GUI
- `main_window.py` - Główne okno z pełną funkcjonalnością
- `dictionary_editor.py` - Dialog edycji słownika
- `translation_editor.py` - Dialog edycji tłumaczeń
- `settings_dialog.py` - Dialog ustawień zaawansowanych

#### Utilities
- `config_manager.py` - Zarządzanie konfiguracją YAML
- Wsparcie dla niestandardowego słownika JSON

#### Dokumentacja
- `README.md` - Kompleksowa dokumentacja użytkownika (polski)
- `QUICKSTART.md` - Przewodnik szybkiego startu (5 minut)
- `USAGE_EXAMPLES.md` - 10 praktycznych przykładów użycia
- `FAQ.md` - Odpowiedzi na najczęściej zadawane pytania
- `TECHNICAL.md` - Dokumentacja techniczna dla deweloperów
- `ARCHITECTURE.md` - Architektura systemu z diagramami
- `CONTRIBUTING.md` - Wytyczne dla kontrybutorów
- `CHANGELOG.md` - Historia zmian

#### Instalacja i Konfiguracja
- `requirements.txt` - Lista wszystkich zależności Python
- `install.sh` - Skrypt instalacyjny dla Linux/Mac
- `install.bat` - Skrypt instalacyjny dla Windows
- `test_installation.py` - Weryfikacja poprawności instalacji
- `config.yaml.template` - Szablon konfiguracji
- `custom_dictionary.json` - Słownik terminów tradingowych
- `setup.py` - Instalator pakietu Python
- `.gitignore` - Pliki do ignorowania przez Git
- `LICENSE` - Licencja MIT

#### Inne
- Struktura katalogów: `src/core/`, `src/gui/`, `src/utils/`
- Katalog `models/` dla automatycznie pobieranych modeli ML

### 🔧 Konfiguracja

#### Domyślne Ustawienia
- Model Whisper: medium
- Urządzenie: CUDA (z fallback na CPU)
- Język źródłowy: angielski
- Język docelowy: polski
- Model TTS: tts_models/pl/mai_female/vits
- Próg ciszy: 0.4s
- Min długość segmentu: 1.0s
- Max długość segmentu: 30.0s
- Dopasowanie tempa: włączone
- Klatki kluczowe: włączone

### 📊 Statystyki Projektu v1.0.0

- **17 plików Python** (~2,738 linii kodu)
- **8 plików dokumentacji** (~35,000+ słów)
- **6 katalogów** w zorganizowanej strukturze
- **15+ głównych klas/modułów**
- **4 dialogi GUI**
- **5 głównych silników** (Whisper, Translate, TTS, Video, Config)

### 🎯 Funkcjonalności

#### Wspierane Formaty
- **Wejście**: MP4, AVI, MKV, MOV
- **Wyjście**: MP4 (H.264 + AAC)

#### Języki
- **Transkrypcja**: Angielski (konfigurowalny)
- **Tłumaczenie**: Angielski → Polski
- **TTS**: Polski (głos żeński)

### 🚀 Wydajność

#### Benchmarki (GPU RTX 3060, Model Medium)
- 1 min wideo: ~2-3 min przetwarzania
- 5 min wideo: ~8-12 min przetwarzania
- 10 min wideo: ~15-25 min przetwarzania
- 30 min wideo: ~45-75 min przetwarzania

### 🛠️ Wymagania Systemowe

#### Minimalne
- Python 3.8+
- 8GB RAM
- 10GB miejsca na dysku
- FFmpeg

#### Zalecane
- Python 3.9-3.10
- 16GB+ RAM
- GPU NVIDIA z CUDA
- 20GB+ miejsca na dysku
- FFmpeg

### 📝 Znane Ograniczenia

- Tłumaczenie wymaga połączenia internetowego (Google Translate API)
- Brak CLI (tylko GUI)
- Brak przetwarzania wsadowego (batch)
- Brak podglądu wideo przed eksportem
- Tylko jeden głos lektora (żeński polski)

### 🔮 Planowane Funkcje (v1.1+)

#### Wysokiej Priorytetu
- [ ] Wybór różnych głosów lektora
- [ ] Eksport transkrypcji (SRT, VTT)
- [ ] CLI interface
- [ ] Batch processing
- [ ] Testy jednostkowe

#### Średniego Priorytetu
- [ ] Więcej modeli TTS
- [ ] Offline translation
- [ ] Video preview
- [ ] Timeline editor
- [ ] Progress saving/resuming

#### Niskiego Priorytetu
- [ ] Real-time processing
- [ ] Cloud processing
- [ ] Mobile app
- [ ] API service
- [ ] Multi-language support

---

## Format Wersjonowania

**MAJOR.MINOR.PATCH**

- **MAJOR**: Zmiany niekompatybilne wstecznie
- **MINOR**: Nowe funkcje kompatybilne wstecz
- **PATCH**: Poprawki błędów kompatybilne wstecz

## Kategorie Zmian

- **Dodano**: Nowe funkcje
- **Zmieniono**: Zmiany w istniejących funkcjach
- **Przestarzałe**: Funkcje które będą usunięte w przyszłości
- **Usunięto**: Usunięte funkcje
- **Poprawiono**: Poprawki błędów
- **Bezpieczeństwo**: Zmiany związane z bezpieczeństwem

---

**Pierwsza stabilna wersja!** 🎉🎬
