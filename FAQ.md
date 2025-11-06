# FAQ - Najczęściej Zadawane Pytania

## Ogólne

### Q: Czy aplikacja jest darmowa?
**A:** Tak, aplikacja jest całkowicie darmowa i open-source (licencja MIT).

### Q: Czy potrzebuję połączenia z internetem?
**A:** 
- **Przy pierwszym uruchomieniu**: TAK - pobierane są modele Whisper i TTS
- **Podczas przetwarzania**: TAK - do tłumaczenia używany jest Google Translate
- **Po pierwszej instalacji**: Modele są lokalnie, ale wciąż potrzebny internet do tłumaczenia

### Q: Czy mogę używać offline?
**A:** Częściowo. Transkrypcja i TTS działają offline, ale tłumaczenie wymaga internetu.

### Q: Ile miejsca na dysku potrzebuję?
**A:** 
- Instalacja podstawowa: ~3GB
- Modele Whisper: 1-5GB (zależnie od rozmiaru)
- Modele TTS: ~100MB
- Miejsce robocze: 2-3x rozmiar przetwarzanego filmu
- **Rekomendacja**: Min. 10GB wolnego miejsca

## Wydajność

### Q: Jak długo trwa przetwarzanie?
**A:** Zależy od:
- Długości filmu
- Modelu Whisper (tiny = szybko, large = wolno)
- GPU vs CPU (GPU 5-10x szybsze)
- Mocy komputera

Przykładowe czasy (GPU RTX 3060, model medium):
- 5 min filmu = ~8-12 min przetwarzania
- 15 min filmu = ~25-35 min przetwarzania
- 30 min filmu = ~45-75 min przetwarzania

### Q: Jak przyspieszyć przetwarzanie?
**A:**
1. Użyj GPU z CUDA (najważniejsze!)
2. Zmniejsz model Whisper (medium → small → base)
3. Zamknij inne programy
4. Zwiększ RAM jeśli to możliwe

### Q: Czy mogę przetwarzać wiele filmów jednocześnie?
**A:** Nie zalecane. Aplikacja używa dużo zasobów GPU/CPU. Przetwarzaj po kolei.

## Problemy Techniczne

### Q: "CUDA niedostępna" - co to znaczy?
**A:** 
Twoja karta graficzna nie jest wykryta lub brak sterowników NVIDIA.

**Rozwiązanie:**
1. Sprawdź czy masz kartę NVIDIA: `nvidia-smi`
2. Zainstaluj najnowsze sterowniki NVIDIA
3. Zainstaluj CUDA Toolkit
4. Reinstaluj PyTorch z CUDA: 
   ```
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

Alternatywnie: Użyj CPU (w ustawieniach zmień device na "cpu")

### Q: "FFmpeg nie znaleziono"
**A:**
**Windows:**
1. Pobierz FFmpeg z https://ffmpeg.org/download.html
2. Rozpakuj
3. Dodaj folder bin do PATH
4. Restart terminala

**Linux:**
```bash
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

### Q: Błąd pamięci (Out of Memory)
**A:**
Twoja karta graficzna/RAM nie ma wystarczająco pamięci.

**Rozwiązanie:**
1. Zmniejsz model Whisper (large → medium → small)
2. Zamknij inne aplikacje
3. Użyj CPU zamiast GPU (wolniejsze, ale mniej pamięci)
4. Przetwarzaj krótsze filmy

### Q: Aplikacja się zawiesza
**A:**
1. Sprawdź logi w sekcji "Logi"
2. Sprawdź czy proces rzeczywiście się zawiesił (może to długo trwa)
3. Restart aplikacji
4. Użyj mniejszego modelu
5. Sprawdź czy plik wideo nie jest uszkodzony

### Q: Słaba jakość transkrypcji
**A:**
**Przyczyny:**
- Słaba jakość audio w filmie
- Zbyt mały model Whisper
- Akcent/dialekt nietypowy

**Rozwiązanie:**
1. Użyj większego modelu (medium → large)
2. Użyj filmu o lepszej jakości audio
3. Upewnij się, że język w ustawieniach to "en"

### Q: Słaba jakość tłumaczenia
**A:**
1. Edytuj słownik - dodaj specjalistyczne terminy
2. Użyj "Podgląd Transkrypcji" → "Edytuj Tłumaczenia"
3. Ręcznie popraw tłumaczenia przed generowaniem lektora

### Q: Głos lektora brzmi dziwnie
**A:**
To normalne dla syntetycznego TTS. Jakość zależy od modelu.

**Możliwe usprawnienia:**
- Popraw interpunkcję w tłumaczeniach (przecinki, kropki)
- Podziel długie zdania na krótsze
- Usuń skróty (np. "mr" → "mister")

### Q: Wideo i audio nie są zsynchronizowane
**A:**
**Sprawdź ustawienia:**
1. Czy "Włącz dopasowanie tempa" jest zaznaczone?
2. Czy "Dodawaj klatki kluczowe" jest zaznaczone?

Jeśli problem występuje nadal:
- Może to być problem z oryginalnym wideo
- Spróbuj przekonwertować wideo do MP4 przed przetwarzaniem

## Funkcjonalność

### Q: Czy mogę wybrać inny głos lektora?
**A:** Obecnie aplikacja używa polskiego głosu żeńskiego. W przyszłości planowane są opcje wyboru głosu.

### Q: Czy mogę zachować oryginalną ścieżkę audio?
**A:** Nie, zgodnie z wymaganiami oryginalny dźwięk jest usuwany i zastąpiony lektorem.

### Q: Czy mogę przetworzyć filmy w innych językach?
**A:** Tak, ale:
- Zmień język źródłowy w ustawieniach (obecnie: angielski)
- Słownik jest zoptymalizowany dla terminologii tradingowej w angielskim
- Tłumaczenie zawsze jest na polski

### Q: Czy mogę dubbing na inne języki niż polski?
**A:** Tak, ale wymaga to modyfikacji:
1. Ustawienia → Translation → Język docelowy: "es" (hiszpański), "de" (niemiecki), etc.
2. Ustawienia → TTS → Znajdź odpowiedni model dla tego języka
3. Kliknij "Zapisz"

### Q: Jak działa słownik niestandardowy?
**A:**
- Słownik zastępuje konkretne słowa/frazy przed tłumaczeniem
- Działa na poziomie całych słów (nie części)
- Case-insensitive (bez względu na wielkość liter)
- Idealny dla terminologii technicznej, która nie powinna być tłumaczona

### Q: Czy mogę eksportować transkrypcję do pliku tekstowego?
**A:** Obecnie nie ma tej funkcji w GUI, ale jest planowana w przyszłych wersjach.

## Formatowanie

### Q: Jakie formaty wideo są obsługiwane?
**A:** 
- **Wejście**: MP4, AVI, MKV, MOV, i większość popularnych formatów
- **Wyjście**: MP4 (H.264)

### Q: Czy mogę zmienić jakość wyjściowego wideo?
**A:** Tak, w Ustawieniach Zaawansowanych można zmienić:
- Codec
- Bitrate
- Format

### Q: Czy wielkość pliku wyjściowego jest większa?
**A:** Zazwyczaj podobna lub nieco mniejsza, bo:
- Tylko jedna ścieżka audio (syntetyczna, skompresowana)
- Możliwa rekomresja wideo

## Instalacja

### Q: Instalacja nie powiodła się - co robić?
**A:**
1. Sprawdź czy masz Python 3.8+
2. Sprawdź czy masz wystarczająco miejsca na dysku
3. Upewnij się że masz prawa administratora (Windows)
4. Spróbuj ręcznej instalacji:
   ```bash
   pip install -r requirements.txt
   ```
5. Jeśli konkretny pakiet się nie instaluje, pomiń go i spróbuj uruchomić aplikację

### Q: Podczas instalacji pip pokazuje błędy
**A:**
- Aktualizuj pip: `pip install --upgrade pip`
- Użyj Python 3.8-3.10 (najlepiej kompatybilne)
- Na Windows może być potrzebny Visual C++ Redistributable

### Q: Skrypt install.sh/install.bat nie działa
**A:**
**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:** 
- Uruchom jako Administrator
- Lub wykonaj kroki ręcznie zgodnie z README.md

## Użytkowanie

### Q: Czy mogę zatrzymać proces dubbingu w trakcie?
**A:** Obecnie nie ma przycisku "Anuluj". Musisz zamknąć aplikację. Pliki tymczasowe zostaną w temp_segments/ - możesz je ręcznie usunąć.

### Q: Gdzie są zapisywane logi?
**A:** Wyświetlane są w aplikacji w sekcji "Logi". Nie są zapisywane do pliku (planowane w przyszłości).

### Q: Czy mogę używać aplikacji z wiersza poleceń (CLI)?
**A:** Obecnie tylko GUI. CLI może być dodane w przyszłości.

### Q: Jak usunąć pliki tymczasowe?
**A:** 
Są automatycznie czyszczone po zakończeniu. Jeśli pozostały (np. po błędzie):
```bash
# Usuń zawartość katalogu
rm -rf temp_segments/*
```

Windows:
```
rmdir /s /q temp_segments
mkdir temp_segments
```

## Bezpieczeństwo i Prywatność

### Q: Czy moje filmy są wysyłane do internetu?
**A:** 
- **NIE** - filmy są przetwarzane lokalnie
- **TAK** - tylko teksty są wysyłane do Google Translate do tłumaczenia
- Audio i wideo nigdy nie opuszczają Twojego komputera

### Q: Czy mogę używać aplikacji do filmów komercyjnych?
**A:** Licencja MIT pozwala na dowolne użycie. Jednak:
- Sprawdź prawa autorskie do oryginalnych filmów
- Sprawdź regulamin serwisów tłumaczeniowych
- Odpowiadasz za zgodność z prawem autorskim

### Q: Czy dane są gromadzone?
**A:** NIE. Aplikacja nie zbiera żadnych danych, nie wysyła statystyk, nie ma telemetrii.

## Aktualizacje

### Q: Jak zaktualizować aplikację?
**A:**
```bash
git pull
pip install -r requirements.txt --upgrade
```

### Q: Jak sprawdzić wersję?
**A:** Otwórz `src/__init__.py` i sprawdź `__version__`

### Q: Czy stare pliki config.yaml są kompatybilne?
**A:** Zazwyczaj tak. Jeśli nie, aplikacja utworzy brakujące klucze z wartościami domyślnymi.

## Wsparcie

### Q: Gdzie zgłosić błąd?
**A:** Utwórz issue na GitHub: https://github.com/stanhrynkiewicz-bot/Filmy/issues

### Q: Gdzie mogę dostać pomoc?
**A:** 
1. Sprawdź README.md
2. Sprawdź FAQ.md (ten plik)
3. Sprawdź USAGE_EXAMPLES.md
4. Utwórz issue na GitHub

### Q: Czy są planowane nowe funkcje?
**A:** Planowane:
- Wybór różnych głosów lektora
- Eksport transkrypcji do SRT/TXT
- CLI (wiersz poleceń)
- Przetwarzanie wsadowe (wiele filmów)
- Więcej opcji TTS
- Offline tłumaczenie (bez internetu)
- Podgląd przed eksportem

---

**Nie znalazłeś odpowiedzi?**

Utwórz issue na GitHub z:
- Dokładnym opisem problemu
- Logami z aplikacji
- Wersją Pythona i systemu operacyjnego
- Informacją o karcie graficznej
