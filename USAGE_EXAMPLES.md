# Przykłady Użycia - Aplikacja do Dubbingu

## Przykład 1: Podstawowe Użycie

### Krok po kroku dla początkujących

```
1. Uruchom aplikację:
   python dubbing_app.py

2. W głównym oknie:
   - Kliknij "Wybierz Film"
   - Wybierz plik: trading_tutorial.mp4

3. Poczekaj aż przycisk "Rozpocznij Dubbing" stanie się aktywny

4. Kliknij "Rozpocznij Dubbing"

5. Obserwuj pasek postępu - proces może zająć kilka minut

6. Po zakończeniu znajdziesz plik:
   output/trading_tutorial_dubbed.mp4
```

## Przykład 2: Z Edycją Słownika

### Dla filmów o tradingu ze specjalistyczną terminologią

```
1. Uruchom aplikację

2. Kliknij "Edytuj Słownik"

3. Dodaj terminy tradingowe:
   - Dodaj pozycję: "scalping" → "scalping"
   - Dodaj pozycję: "swing trade" → "swing trading"
   - Dodaj pozycję: "stop loss" → "stop loss"
   - Kliknij "Zapisz"

4. Wybierz film

5. Rozpocznij dubbing - twoje terminy będą zachowane
```

## Przykład 3: Z Podglądem i Edycją Tłumaczeń

### Dla perfekcjonistów chcących kontrolować tłumaczenia

```
1. Uruchom aplikację

2. Wybierz film: forex_strategy.mp4

3. Kliknij "Podgląd Transkrypcji"
   - Zobacz wykryte segmenty dialogu
   - Sprawdź czy wszystko zostało dobrze rozpoznane

4. Kliknij "Edytuj Tłumaczenia"
   - Przejrzyj automatyczne tłumaczenia
   - Popraw te, które wymagają korekty
   - Kliknij "Zapisz Zmiany"

5. Kliknij "Rozpocznij Dubbing"
   - Twoje poprawki zostaną użyte w lektorze
```

## Przykład 4: Dostosowanie Ustawień dla Szybkiego Przetwarzania

### Gdy zależy ci na czasie

```
1. Uruchom aplikację

2. Przejdź do zakładki "Ustawienia"

3. W "Szybkie Ustawienia":
   - Model Whisper: Zmień na "small" lub "base"
   - CUDA: Upewnij się że jest zaznaczone
   - Kliknij "Zapisz Ustawienia"

4. Wróć do zakładki "Główna"

5. Wybierz film i rozpocznij dubbing
   - Będzie szybciej, ale jakość transkrypcji może być nieco niższa
```

## Przykład 5: Najwyższa Jakość (wolniejsze)

### Dla najważniejszych filmów

```
1. Uruchom aplikację

2. Zakładka "Ustawienia" → "Otwórz Ustawienia Zaawansowane"

3. Zakładka "Whisper":
   - Model: "large"
   
4. Zakładka "Wideo":
   - Min. długość segmentu: 2.0s
   - Max. długość segmentu: 20.0s
   - Włącz dopasowanie tempa: TAK
   - Dodawaj klatki kluczowe: TAK

5. Kliknij "Zapisz"

6. Wybierz film i rozpocznij dubbing
```

## Przykład 6: Przetwarzanie Serii Filmów

### Workflow dla wielu filmów

```
Dla każdego filmu:

1. Wybierz film_1.mp4
2. Rozpocznij dubbing
3. Poczekaj na zakończenie
4. Wybierz film_2.mp4
5. Rozpocznij dubbing
...

Uwagi:
- Słownik i ustawienia są zachowane między sesjami
- Edytowane tłumaczenia NIE są zachowane (specyficzne dla każdego filmu)
- Wszystkie pliki znajdziesz w output/
```

## Przykład 7: Diagnostyka Problemów

### Gdy coś nie działa

```
1. Uruchom aplikację

2. Spróbuj przetworzyć krótki film testowy (1-2 min)

3. Obserwuj sekcję "Logi":
   - Zielone komunikaty = OK
   - Czerwone = problemy

4. Typowe problemy:
   
   "CUDA nie dostępna":
   - Przejdź do Ustawień
   - Zmień urządzenie na "cpu"
   - Zapisz i spróbuj ponownie
   
   "Błąd podczas transkrypcji":
   - Zmień model Whisper na mniejszy (small/base)
   - Upewnij się że plik wideo jest prawidłowy
   
   "Błąd pamięci":
   - Zamknij inne aplikacje
   - Użyj mniejszego modelu Whisper
   - Rozważ użycie CPU zamiast CUDA
```

## Przykład 8: Tylko Transkrypcja (bez dubbingu)

### Gdy chcesz tylko zobaczyć co zostało rozpoznane

```
1. Uruchom aplikację

2. Wybierz film

3. Kliknij "Podgląd Transkrypcji"

4. Przeczytaj wyniki w oknie dialogowym

5. Opcjonalnie: Kliknij "Edytuj Tłumaczenia" aby zobaczyć tłumaczenia

6. NIE musisz klikać "Rozpocznij Dubbing" jeśli nie chcesz tworzyć pliku wyjściowego
```

## Przykład 9: Zmiana Lokalizacji Wyjściowej

### Gdy chcesz zapisać plik w konkretnym miejscu

```
1. Uruchom aplikację

2. Wybierz film wejściowy

3. Kliknij "Wybierz Lokalizację" (przy pliku wyjściowym)

4. Wybierz folder i nazwę pliku:
   Np. D:\Moje_Filmy\trading_dubbed_final.mp4

5. Rozpocznij dubbing
```

## Przykład 10: Backup i Przywracanie Słownika

### Zachowanie swojej pracy

```
Backup:
1. Znajdź plik: custom_dictionary.json
2. Skopiuj go w bezpieczne miejsce
3. Nazwa przykładowa: dictionary_backup_2024.json

Przywracanie:
1. Skopiuj backup z powrotem jako: custom_dictionary.json
2. Uruchom aplikację
3. Twój słownik zostanie wczytany automatycznie
```

## Wskazówki Ogólne

### Dla najlepszych rezultatów:

1. **Jakość wejścia**:
   - Używaj filmów o dobrej jakości audio
   - Unikaj filmów z dużym szumem tła
   - Preferuj filmy z wyraźną mową

2. **Wydajność**:
   - Pierwsze uruchomienie = najdłuższe (pobieranie modeli)
   - Kolejne uruchomienia są szybsze
   - CUDA jest 5-10x szybsze niż CPU

3. **Słownik**:
   - Dodaj terminy PRZED przetwarzaniem filmu
   - Używaj małych liter dla lepszego dopasowania
   - Słownik działa dla całych słów (nie części słów)

4. **Edycja tłumaczeń**:
   - Edytuj tylko te, które są niepoprawne
   - Możesz poprawić ortografię i gramatykę
   - Krótsze teksty = szybsze generowanie głosu

5. **Ustawienia**:
   - Model "medium" to dobry kompromis jakość/szybkość
   - Model "large" tylko dla krytycznych filmów
   - Model "tiny" gdy potrzebujesz szybko sprawdzić coś

6. **Miejsce na dysku**:
   - Upewnij się że masz min. 2-3x więcej miejsca niż rozmiar filmu
   - Pliki tymczasowe są usuwane automatycznie po zakończeniu
   - Katalog output/ może rosnąć - okresowo czyść stare pliki
