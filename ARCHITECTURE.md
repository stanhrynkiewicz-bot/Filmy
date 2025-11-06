# Architektura Aplikacji do Dubbingu

## Przegląd Architektury

```
┌────────────────────────────────────────────────────────────────────┐
│                        WARSTWA GUI (PyQt5)                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Main Window    │  │ Dictionary Editor│  │Translation Editor│ │
│  │                 │  │                  │  │                  │ │
│  │ • File picker   │  │ • EN→PL terms   │  │ • Preview trans  │ │
│  │ • Progress bar  │  │ • Add/Edit/Del  │  │ • Manual editing │ │
│  │ • Logs display  │  │ • Save/Load     │  │ • Status tracking│ │
│  │ • Settings      │  └──────────────────┘  └──────────────────┘ │
│  └────────┬────────┘                                              │
│           │                                                        │
│  ┌────────┴────────┐                                              │
│  │Settings Dialog  │                                              │
│  │                 │                                              │
│  │ • Whisper cfg   │                                              │
│  │ • TTS cfg       │                                              │
│  │ • Video cfg     │                                              │
│  │ • Paths         │                                              │
│  └─────────────────┘                                              │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                    WARSTWA LOGIKI (Core)                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   Dubbing Engine                              │ │
│  │                                                               │ │
│  │  Orchestrator całego procesu dubbingu:                       │ │
│  │  1. Extract audio        6. Generate TTS                     │ │
│  │  2. Transcribe          7. Process video segments            │ │
│  │  3. Optimize segments   8. Tempo adjustment                  │ │
│  │  4. Translate           9. Combine segments                  │ │
│  │  5. Apply edits        10. Output final video                │ │
│  └────┬─────────────────────────────────────────────────┬────────┘ │
│       │                                                  │          │
│  ┌────┴─────────┐  ┌─────────────┐  ┌─────────────┐   │          │
│  │Transcription │  │ Translation │  │     TTS     │   │          │
│  │   Engine     │  │   Engine    │  │   Engine    │   │          │
│  │              │  │             │  │             │   │          │
│  │• Whisper API │  │• Google API │  │• Coqui TTS  │   │          │
│  │• CUDA support│  │• Dictionary │  │• Polish voice│  │          │
│  │• Segmentation│  │• Batch proc │  │• Batch gen  │   │          │
│  └──────────────┘  └─────────────┘  └─────────────┘   │          │
│                                                         │          │
│  ┌──────────────────────────────────────────────────────┘          │
│  │              Video Processor                                    │
│  │                                                                 │
│  │ • Extract/combine audio      • Tempo adjustment                │
│  │ • Segment video              • Add keyframes                   │
│  │ • Remove silence             • Pad with silence                │
│  │ • Concatenate segments       • Final encoding                  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    WARSTWA UTILITIES                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐                                              │
│  │  Config Manager  │                                              │
│  │                  │                                              │
│  │ • Load YAML      │                                              │
│  │ • Save settings  │                                              │
│  │ • Get/Set values │                                              │
│  │ • Dictionary I/O │                                              │
│  └──────────────────┘                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Przepływ Danych

### 1. Input Stage

```
Video File (MP4/AVI/MKV)
         │
         ▼
    ┌─────────┐
    │ Extract │ ──→ Audio File (WAV)
    │  Audio  │
    └─────────┘
```

### 2. Transcription Stage

```
Audio File
    │
    ▼
┌──────────┐
│ Whisper  │
│  Model   │ ──→ Raw Segments
│  (CUDA)  │     [id, start, end, text]
└──────────┘
    │
    ▼
┌──────────┐
│ Optimize │
│ Segments │
└──────────┘
    │
    ├─→ Merge short segments (< 1s)
    │
    └─→ Split long segments (> 30s)
    │
    ▼
Optimized Segments
```

### 3. Translation Stage

```
Segments with English text
    │
    ▼
┌─────────────┐
│   Apply     │
│ Dictionary  │ ──→ Replace trading terms
└─────────────┘
    │
    ▼
┌─────────────┐
│  Google     │
│ Translate   │ ──→ EN → PL translation
└─────────────┘
    │
    ▼
┌─────────────┐
│   Manual    │
│    Edits    │ ──→ User corrections (optional)
└─────────────┘
    │
    ▼
Segments with Polish translations
```

### 4. TTS Generation Stage

```
Segments with Polish text
    │
    ▼
┌─────────────┐
│  Coqui TTS  │
│  (Polish)   │ ──→ Audio files for each segment
└─────────────┘     [segment_0000.wav, segment_0001.wav, ...]
    │
    ▼
Segments with audio_path + audio_duration
```

### 5. Video Processing Stage

```
For Each Segment:
    │
    ▼
┌─────────────┐
│  Cut Video  │
│   Segment   │ ──→ video_segment.mp4
└─────────────┘
    │
    ▼
Decision Point: video_duration vs audio_duration
    │
    ├─→ IF video < audio:
    │   │
    │   ▼
    │   ┌──────────────┐
    │   │Add Keyframes │
    │   └──────────────┘
    │   │
    │   ▼
    │   ┌──────────────┐
    │   │Adjust Tempo  │ ──→ Speed up/slow down video
    │   └──────────────┘
    │   │
    │   ▼
    │   Video matches audio duration
    │
    └─→ ELSE (video >= audio):
        │
        ▼
        ┌──────────────┐
        │ Pad Audio    │ ──→ Add silence to end
        └──────────────┘
        │
        ▼
        Audio matches video duration
    │
    ▼
┌─────────────┐
│   Combine   │
│ Video+Audio │ ──→ processed_segment.mp4
└─────────────┘
```

### 6. Final Assembly Stage

```
All Processed Segments
    │
    ▼
┌─────────────┐
│ Concatenate │
│  Segments   │ ──→ Single video file
└─────────────┘
    │
    ▼
┌─────────────┐
│   Encode    │
│   (H.264)   │ ──→ final_output.mp4
└─────────────┘
```

## Struktura Modułów

### Core Modules

```
src/core/
├── __init__.py
├── dubbing_engine.py        [MAIN ORCHESTRATOR]
│   └── DubbingEngine
│       ├── process_video()
│       ├── _process_video_segments()
│       └── _combine_segments()
│
├── transcription.py          [WHISPER WRAPPER]
│   └── TranscriptionEngine
│       ├── transcribe_audio()
│       ├── get_segments()
│       ├── merge_short_segments()
│       └── split_long_segments()
│
├── translation.py            [TRANSLATION SERVICE]
│   └── TranslationEngine
│       ├── translate_text()
│       ├── translate_segments()
│       └── _apply_dictionary()
│
├── tts.py                    [TEXT-TO-SPEECH]
│   └── TTSEngine
│       ├── generate_speech()
│       └── generate_speech_batch()
│
└── video_processor.py        [VIDEO OPERATIONS]
    └── VideoProcessor
        ├── extract_audio()
        ├── create_video_segment()
        ├── adjust_video_tempo()
        ├── add_keyframes_to_video()
        ├── combine_video_audio()
        └── pad_audio_with_silence()
```

### GUI Modules

```
src/gui/
├── __init__.py
├── main_window.py            [MAIN APPLICATION WINDOW]
│   ├── MainWindow
│   └── DubbingWorker (QThread)
│
├── dictionary_editor.py      [CUSTOM DICTIONARY EDITOR]
│   └── DictionaryEditor (QDialog)
│
├── translation_editor.py     [MANUAL TRANSLATION EDITOR]
│   └── TranslationEditor (QDialog)
│
└── settings_dialog.py        [ADVANCED SETTINGS]
    └── SettingsDialog (QDialog)
```

### Utility Modules

```
src/utils/
├── __init__.py
└── config_manager.py         [CONFIGURATION MANAGEMENT]
    └── ConfigManager
        ├── load_config()
        ├── save_config()
        ├── get()
        ├── set()
        ├── load_custom_dictionary()
        └── save_custom_dictionary()
```

## Wzorce Projektowe

### 1. Facade Pattern
`DubbingEngine` ukrywa złożoność procesu dubbingu za prostym interfejsem `process_video()`.

### 2. Strategy Pattern
Różne silniki (Whisper, Google Translate, Coqui TTS) mogą być łatwo wymieniane.

### 3. Observer Pattern
GUI używa callback `progress_callback` do śledzenia postępu.

### 4. Template Method
Przetwarzanie segmentów następuje według ustalonego szablonu:
- Extract → Transcribe → Translate → TTS → Process → Combine

## Wydajność i Optymalizacja

### Bottlenecks

1. **Whisper Transcription** (30-40% czasu)
   - Optymalizacja: Mniejszy model, CUDA

2. **TTS Generation** (20-30% czasu)
   - Optymalizacja: Batch processing, cache

3. **Video Processing** (30-40% czasu)
   - Optymalizacja: Parallel processing, hardware encoding

### Memory Management

```
Proces            │ RAM Usage    │ VRAM Usage (CUDA)
──────────────────┼──────────────┼──────────────────
Whisper (medium)  │ 2-4 GB       │ 2-3 GB
TTS               │ 1-2 GB       │ 1 GB
Video Processing  │ 2-4 GB       │ N/A
Peak Usage        │ 6-8 GB       │ 3-4 GB
```

## Security & Privacy

### Data Flow

```
┌──────────────┐
│ Local Video  │ ──────┐
└──────────────┘       │
                       │
┌──────────────┐       │     ┌─────────────────┐
│ Local Audio  │ ──────┼────→│ Local Whisper   │
└──────────────┘       │     └─────────────────┘
                       │
┌──────────────┐       │     ┌─────────────────┐
│ Text Only    │ ──────┼────→│ Google Translate│ (INTERNET)
└──────────────┘       │     └─────────────────┘
                       │
┌──────────────┐       │     ┌─────────────────┐
│ Local Audio  │←──────┼─────│ Local TTS       │
└──────────────┘       │     └─────────────────┘
                       │
┌──────────────┐       │
│ Output Video │←──────┘
└──────────────┘

Tylko tekst jest wysyłany do internetu!
Video i audio pozostają lokalne.
```

## Error Handling

### Hierarchia Błędów

```
Exception
    │
    ├─→ TranscriptionError
    │   ├─→ WhisperLoadError
    │   └─→ AudioProcessingError
    │
    ├─→ TranslationError
    │   └─→ APIConnectionError
    │
    ├─→ TTSError
    │   ├─→ ModelLoadError
    │   └─→ GenerationError
    │
    └─→ VideoProcessingError
        ├─→ SegmentationError
        ├─→ TempoAdjustmentError
        └─→ CombineError
```

### Recovery Strategies

1. **Transcription Fail**: Retry z mniejszym modelem
2. **Translation Fail**: Cache + retry
3. **TTS Fail**: Skip segment + silence
4. **Video Fail**: Save partial results

## Deployment

### Distribution

```
Application Package
    │
    ├─→ Windows: EXE (PyInstaller)
    ├─→ Linux: AppImage / .deb
    └─→ Mac: .app / DMG
```

### Installation Modes

1. **Developer**: Git clone + pip install
2. **User**: Standalone installer
3. **Server**: Docker container (future)

---

**Dokumentacja architektury v1.0**
