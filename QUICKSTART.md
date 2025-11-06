# Szybki Start - 5 minut do pierwszego dubbingu

## 🚀 Błyskawiczna Instalacja

### Windows
```cmd
# 1. Pobierz repozytorium
git clone https://github.com/stanhrynkiewicz-bot/Filmy.git
cd Filmy

# 2. Uruchom instalator
install.bat

# 3. Gotowe!
```

### Linux/Mac
```bash
# 1. Pobierz repozytorium
git clone https://github.com/stanhrynkiewicz-bot/Filmy.git
cd Filmy

# 2. Uruchom instalator
chmod +x install.sh
./install.sh

# 3. Gotowe!
```

## ⚡ Pierwsze Uruchomienie

```bash
# Aktywuj środowisko
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Uruchom aplikację
python dubbing_app.py
```

## 🎬 Pierwszy Dubbing w 4 Krokach

1. **Wybierz Film**
   - Kliknij przycisk "Wybierz Film"
   - Wybierz plik MP4/AVI/MKV

2. **Opcjonalnie: Edytuj Słownik**
   - Kliknij "Edytuj Słownik"
   - Dodaj terminy tradingowe
   - Zapisz

3. **Rozpocznij**
   - Kliknij "Rozpocznij Dubbing"
   - Poczekaj (może potrwać kilka minut)

4. **Gotowe!**
   - Plik znajdziesz w katalogu `output/`

## 📊 Przykład: Film 5-minutowy

**Proces:**
```
[00:00] Wybór filmu...
[00:10] Rozpoczęto przetwarzanie
[01:00] Transkrypcja (Whisper)
[03:00] Tłumaczenie
[05:00] Generowanie lektora (TTS)
[08:00] Przetwarzanie wideo
[10:00] Gotowe!
```

**Rezultat:** Film z polskim lektorem w `output/nazwa_filmu_dubbed.mp4`

## 🔧 Podstawowe Ustawienia

### Dla szybkości (niższa jakość):
```
Zakładka "Ustawienia":
- Model Whisper: "small"
- CUDA: ✓ (jeśli dostępne)
```

### Dla najlepszej jakości:
```
Zakładka "Ustawienia":
- Model Whisper: "medium" lub "large"
- CUDA: ✓
- Dopasowanie tempa: ✓
- Klatki kluczowe: ✓
```

## ❗ Najczęstsze Problemy

### "CUDA niedostępna"
**Rozwiązanie:**
```
Zakładka "Ustawienia" → Odznacz "Użyj CUDA (GPU)"
```

### "FFmpeg nie znaleziono"
**Windows:** Pobierz FFmpeg, dodaj do PATH, restart  
**Linux:** `sudo apt install ffmpeg`  
**Mac:** `brew install ffmpeg`

### Wolne przetwarzanie
- Użyj mniejszego modelu Whisper (small/base)
- Włącz CUDA jeśli masz kartę NVIDIA
- Przetwarzaj krótsze filmy

## 📚 Dalsze Kroki

- 📖 Przeczytaj [README.md](README.md) dla pełnej dokumentacji
- 💡 Zobacz [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) dla zaawansowanych przykładów
- ❓ Sprawdź [FAQ.md](FAQ.md) jeśli masz pytania

## 🎯 Krótkie Wskazówki

✅ **Zrób:**
- Używaj filmów o dobrej jakości audio
- Edytuj słownik dla specjalistycznych terminów
- Zapisuj ustawienia po zmianie

❌ **Unikaj:**
- Filmów z dużym szumem tła
- Zamykania aplikacji podczas przetwarzania
- Przetwarzania wielu filmów jednocześnie

## 💪 To Proste!

1. Wybierz film
2. Kliknij "Rozpocznij Dubbing"
3. Poczekaj
4. Gotowe!

**Powodzenia z dubbingiem Twoich filmów o tradingu! 🎬🎙️**
