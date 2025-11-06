# Dokumentacja Techniczna

## Architektura Aplikacji

### Przegląd

```
┌─────────────────────────────────────────────────────────┐
│                    GUI (PyQt5)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Main Window  │  │ Dict Editor  │  │ Trans Editor │  │
│  └──────┬───────┘  └──────────────┘  └──────────────┘  │
│         │                                                │
└─────────┼────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              Dubbing Engine (Core)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │Transcription │  │ Translation  │  │     TTS      │  │
│  │  (Whisper)   │  │   (Google)   │  │  (Coqui)     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Video Processor (MoviePy)                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              Utilities & Config                          │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │Config Manager│  │  Dictionary  │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## Moduły

### 1. GUI Layer (`src/gui/`)

#### `main_window.py`
**Główne okno aplikacji**

Klasy:
- `MainWindow`: Główne okno aplikacji z zakładkami
- `DubbingWorker`: QThread dla procesu dubbingu w tle

Funkcjonalności:
- Wybór plików wejściowych/wyjściowych
- Zarządzanie ustawieniami
- Wyświetlanie postępu
- Logowanie zdarzeń

#### `dictionary_editor.py`
**Dialog edycji słownika**

Klasy:
- `DictionaryEditor`: QDialog z tabelą do edycji par klucz-wartość

#### `translation_editor.py`
**Dialog edycji tłumaczeń**

Klasy:
- `TranslationEditor`: QDialog z tabelą segmentów i ich tłumaczeń

#### `settings_dialog.py`
**Dialog ustawień zaawansowanych**

Klasy:
- `SettingsDialog`: QDialog z zakładkami dla różnych kategorii ustawień

### 2. Core Layer (`src/core/`)

#### `dubbing_engine.py`
**Główny orchestrator procesu**

Klasy:
- `DubbingEngine`: Koordynuje cały proces dubbingu

Metody kluczowe:
```python
def process_video(self, video_path, output_path, 
                 custom_dictionary, edited_translations) -> bool
```

Pipeline:
1. Ekstrakcja audio
2. Transkrypcja (Whisper)
3. Optymalizacja segmentów
4. Tłumaczenie
5. Generowanie TTS
6. Przetwarzanie segmentów wideo
7. Łączenie finalnego filmu

#### `transcription.py`
**Moduł transkrypcji**

Klasy:
- `TranscriptionEngine`: Wrapper dla Whisper

Kluczowe metody:
```python
def transcribe_audio(self, audio_path: str) -> Dict
def get_segments(self, transcription_result: Dict) -> List[Dict]
def merge_short_segments(self, segments: List[Dict]) -> List[Dict]
def split_long_segments(self, segments: List[Dict]) -> List[Dict]
```

#### `translation.py`
**Moduł tłumaczenia**

Klasy:
- `TranslationEngine`: Wrapper dla deep-translator

Funkcjonalności:
- Tłumaczenie z Google Translate
- Zastosowanie słownika niestandardowego
- Batch processing

#### `tts.py`
**Moduł Text-to-Speech**

Klasy:
- `TTSEngine`: Wrapper dla Coqui TTS

Kluczowe metody:
```python
def generate_speech(self, text: str, output_path: str) -> str
def generate_speech_batch(self, segments: list, output_dir: str) -> list
```

#### `video_processor.py`
**Moduł przetwarzania wideo**

Klasy:
- `VideoProcessor`: Operacje na wideo i audio

Funkcjonalności:
- Ekstrakcja/łączenie audio
- Segmentacja wideo
- Dopasowanie tempa
- Dodawanie klatek kluczowych
- Padding audio ciszą

### 3. Utils Layer (`src/utils/`)

#### `config_manager.py`
**Zarządzanie konfiguracją**

Klasy:
- `ConfigManager`: YAML config management

Metody:
```python
def load_config(self) -> Dict
def save_config(self) -> bool
def get(self, key: str, default: Any) -> Any
def set(self, key: str, value: Any)
```

## Przepływ Danych

### Struktura Segmentu

```python
segment = {
    'id': int,                    # ID segmentu
    'start': float,               # Czas rozpoczęcia (s)
    'end': float,                 # Czas zakończenia (s)
    'text': str,                  # Tekst oryginalny (EN)
    'translated_text': str,       # Tekst przetłumaczony (PL)
    'audio_path': str,            # Ścieżka do pliku audio TTS
    'audio_duration': float       # Długość audio (s)
}
```

### Pipeline Przetwarzania

```
Video Input
    ↓
[Extract Audio] → audio.wav
    ↓
[Whisper Transcription] → segments[]
    ↓
[Optimize Segments] → merged/split segments[]
    ↓
[Apply Dictionary] → custom terms applied
    ↓
[Google Translate] → translated_text in segments[]
    ↓
[Apply Manual Edits] → edited translations
    ↓
[TTS Generation] → audio_path in segments[]
    ↓
[Video Segmentation] → video segments
    ↓
[Process Each Segment]:
    IF video_duration < audio_duration:
        [Add Keyframes]
        [Adjust Tempo] → match audio_duration
    ELSE:
        [Pad Audio with Silence] → match video_duration
    [Combine Video + Audio] → processed segment
    ↓
[Concatenate All Segments] → final_output.mp4
```

## Algorytmy

### 1. Dopasowanie Tempa Wideo

```python
def adjust_video_tempo(video_path, target_duration, output_path):
    original_duration = get_duration(video_path)
    speed_factor = original_duration / target_duration
    
    # speed_factor > 1.0 → przyśpieszenie
    # speed_factor < 1.0 → spowolnienie
    
    adjusted = video.fx(speedx(speed_factor))
    save(adjusted, output_path)
```

### 2. Optymalizacja Segmentów

**Łączenie krótkich:**
```python
def merge_short_segments(segments, min_duration):
    merged = []
    current = segments[0]
    
    for next_seg in segments[1:]:
        if (current.end - current.start) < min_duration:
            # Połącz z następnym
            current.end = next_seg.end
            current.text += " " + next_seg.text
        else:
            merged.append(current)
            current = next_seg
    
    return merged
```

**Dzielenie długich:**
```python
def split_long_segments(segments, max_duration):
    result = []
    
    for seg in segments:
        if (seg.end - seg.start) > max_duration:
            # Podziel na zdania
            sentences = split_sentences(seg.text)
            # Przydziel czas proporcjonalnie
            # ...
        else:
            result.append(seg)
    
    return result
```

### 3. Usuwanie Ciszy

```python
def remove_short_silence(audio, min_silence_len=400, threshold=-40):
    # Wykryj fragmenty z dźwiękiem
    nonsilent = detect_nonsilent(audio, min_silence_len, threshold)
    
    # Wytnij i połącz fragmenty bez ciszy
    chunks = [audio[start:end] for start, end in nonsilent]
    result = concatenate(chunks)
    
    return result
```

## Konfiguracja

### Format YAML

```yaml
whisper:
  model_size: "medium"    # tiny, base, small, medium, large
  device: "cuda"          # cuda, cpu
  language: "en"          # en, pl, de, es, etc.

translation:
  source_lang: "en"
  target_lang: "pl"
  service: "google"       # google (więcej w przyszłości)

tts:
  model_name: "tts_models/pl/mai_female/vits"
  speaker: null
  language: "pl"

video:
  silence_threshold: 0.4           # s
  min_segment_duration: 1.0        # s
  max_segment_duration: 30.0       # s
  tempo_adjustment_enabled: true
  add_keyframes: true

audio:
  sample_rate: 16000
  silence_threshold_db: -40

output:
  format: "mp4"
  codec: "libx264"
  audio_codec: "aac"
  bitrate: "5000k"

paths:
  temp_dir: "temp_segments"
  output_dir: "output"
  cache_dir: "cache"
  models_dir: "models"
  dictionary_file: "custom_dictionary.json"
```

## Zależności

### Główne Biblioteki

| Biblioteka | Wersja | Cel |
|------------|--------|-----|
| whisper | 20231117+ | Transkrypcja audio |
| torch | 2.0.0+ | Backend ML (CUDA) |
| TTS | 0.22.0+ | Text-to-Speech |
| PyQt5 | 5.15.9+ | GUI |
| moviepy | 1.0.3+ | Przetwarzanie wideo |
| pydub | 0.25.1+ | Przetwarzanie audio |
| deep-translator | 1.11.4+ | Tłumaczenie |

### Wymagania Systemowe

**Minimalne:**
- Python 3.8+
- 8GB RAM
- 10GB miejsca na dysku

**Zalecane:**
- Python 3.9-3.10
- 16GB RAM
- GPU NVIDIA z CUDA
- 20GB miejsca na dysku

## Wydajność

### Benchmarki (GPU RTX 3060, Model Medium)

| Długość Video | Czas Przetwarzania | Współczynnik |
|---------------|-------------------|--------------|
| 1 min | 2-3 min | ~2.5x |
| 5 min | 8-12 min | ~2.0x |
| 10 min | 15-25 min | ~2.0x |
| 30 min | 45-75 min | ~2.0x |

### Optymalizacja

**Dla szybkości:**
- Model Whisper: tiny/base
- Device: CUDA
- Pomiń edycję tłumaczeń

**Dla jakości:**
- Model Whisper: large
- Device: CUDA
- Edytuj słownik + tłumaczenia
- Włącz wszystkie opcje wideo

## Rozszerzalność

### Dodawanie Nowego Serwisu Tłumaczenia

```python
# src/core/translation.py

class TranslationEngine:
    def __init__(self, service="google"):
        if service == "google":
            self.translator = GoogleTranslator(...)
        elif service == "deepl":  # NOWY
            self.translator = DeepLTranslator(...)
        # ...
```

### Dodawanie Nowego Modelu TTS

```python
# src/core/tts.py

class TTSEngine:
    def __init__(self, model_name):
        if "coqui" in model_name:
            self.tts = CoquiTTS(model_name)
        elif "custom" in model_name:  # NOWY
            self.tts = CustomTTS(model_name)
        # ...
```

### Dodawanie Nowych Języków

1. Dodaj do `config.yaml`:
   ```yaml
   translation:
     source_lang: "de"  # niemiecki
     target_lang: "pl"
   ```

2. Znajdź model TTS dla tego języka:
   ```yaml
   tts:
     model_name: "tts_models/de/thorsten/vits"
   ```

## Testowanie

### Unit Tests (TODO)

```bash
pytest tests/
```

### Integration Tests (TODO)

```bash
pytest tests/integration/
```

### Testowanie Instalacji

```bash
python test_installation.py
```

## Debugowanie

### Włączenie Verbose Logging

```python
# W dubbing_engine.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Analiza Logów

Logi wyświetlane w GUI w sekcji "Logi" zawierają:
- Postęp każdego kroku
- Błędy z traceback
- Ostrzeżenia o potencjalnych problemach

### Typowe Problemy

1. **CUDA Out of Memory**
   - Zmniejsz model
   - Użyj CPU
   - Zwiększ VRAM

2. **FFmpeg Error**
   - Sprawdź instalację
   - Sprawdź format wideo
   - Sprawdź uprawnienia do plików

3. **TTS Error**
   - Sprawdź połączenie internetowe (pierwsze uruchomienie)
   - Sprawdź dostępność modelu
   - Sprawdź logi Coqui TTS

## Licencje Komponentów

- **Whisper**: MIT (OpenAI)
- **TTS**: MPL 2.0 (Coqui)
- **PyQt5**: GPL v3
- **MoviePy**: MIT
- **Deep Translator**: Apache 2.0

## Roadmap

### v1.1 (Planowane)
- [ ] Wybór różnych głosów lektora
- [ ] Eksport transkrypcji (SRT, TXT)
- [ ] CLI interface
- [ ] Batch processing

### v1.2 (Planowane)
- [ ] Offline translation
- [ ] Custom TTS models
- [ ] Video preview
- [ ] Timeline editor

### v2.0 (Wizja)
- [ ] Real-time processing
- [ ] Cloud processing
- [ ] Mobile app
- [ ] API service

## Kontrybuowanie

Przeczytaj CONTRIBUTING.md (TODO) dla wytycznych dotyczących kontrybuowania do projektu.

---

**Aktualizacja dokumentacji:** 2024-11-03
