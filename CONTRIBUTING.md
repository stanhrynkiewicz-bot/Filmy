# Wytyczne Kontrybuowania

Dziękujemy za zainteresowanie rozwojem aplikacji do dubbingu filmów! 🎉

## Jak Przyczynić się do Projektu

### 🐛 Zgłaszanie Błędów

1. Sprawdź czy błąd nie został już zgłoszony w [Issues](https://github.com/stanhrynkiewicz-bot/Filmy/issues)
2. Utwórz nowy issue z:
   - Dokładnym opisem problemu
   - Krokami do reprodukcji
   - Oczekiwanym vs rzeczywistym zachowaniem
   - Logami z aplikacji
   - Informacjami o systemie (OS, Python, GPU)

### 💡 Proponowanie Funkcji

1. Otwórz issue z etykietą "enhancement"
2. Opisz:
   - Jaki problem rozwiązuje ta funkcja
   - Jak miałaby działać
   - Dlaczego byłaby użyteczna

### 🔧 Pull Requests

#### Przed Rozpoczęciem

1. Fork repozytorium
2. Utwórz nową gałąź: `git checkout -b feature/nazwa-funkcji`
3. Upewnij się że rozumiesz architekturę (przeczytaj TECHNICAL.md)

#### Podczas Pracy

1. Trzymaj się stylu kodu:
   - PEP 8 dla Pythona
   - Komentarze w języku polskim lub angielskim
   - Docstringi dla wszystkich funkcji/klas

2. Testuj swoje zmiany:
   ```bash
   python test_installation.py
   python dubbing_app.py  # Test manualny
   ```

3. Aktualizuj dokumentację jeśli potrzeba

#### Przesyłanie PR

1. Commit z jasnym opisem:
   ```bash
   git commit -m "Dodano: [krótki opis funkcji]"
   ```

2. Push do swojego forka:
   ```bash
   git push origin feature/nazwa-funkcji
   ```

3. Utwórz Pull Request z:
   - Opisem zmian
   - Odnośnikami do powiązanych issues
   - Screenshots (jeśli zmiany w GUI)

## Obszary do Kontrybuowania

### 🎯 Priorytet Wysoki

- [ ] Testy jednostkowe i integracyjne
- [ ] Obsługa błędów i recovery
- [ ] Optymalizacja wydajności
- [ ] Wsparcie dla więcej języków
- [ ] CLI interface

### 📋 Priorytet Średni

- [ ] Więcej modeli TTS
- [ ] Wybór różnych głosów lektora
- [ ] Eksport transkrypcji (SRT, VTT)
- [ ] Batch processing (wiele filmów)
- [ ] Podgląd przed eksportem

### 💭 Pomysły na Przyszłość

- [ ] Real-time preview
- [ ] Cloud processing
- [ ] Mobile app
- [ ] API service
- [ ] Wsparcie dla więcej serwisów tłumaczenia

## Struktura Projektu

```
Filmy/
├── src/
│   ├── core/          # Logika biznesowa
│   ├── gui/           # Interfejs użytkownika
│   └── utils/         # Narzędzia pomocnicze
├── tests/             # Testy (TODO)
├── docs/              # Dokumentacja
└── examples/          # Przykłady użycia (TODO)
```

## Style Guide

### Python

```python
class MyClass:
    """Krótki opis klasy
    
    Dłuższy opis co robi ta klasa
    i jak jej używać.
    """
    
    def my_method(self, param: str) -> bool:
        """Krótki opis metody
        
        Args:
            param: Opis parametru
            
        Returns:
            Opis wartości zwracanej
        """
        # Implementacja
        pass
```

### Commit Messages

- **Dodano:** Nowa funkcjonalność
- **Poprawiono:** Bug fix
- **Zmieniono:** Modyfikacja istniejącej funkcji
- **Usunięto:** Usunięcie kodu/funkcji
- **Refaktor:** Refaktoryzacja bez zmiany funkcjonalności
- **Docs:** Zmiany w dokumentacji

### GUI

- Używaj PyQt5
- Trzymaj się Windows-style look and feel
- Wszystkie teksty w języku polskim
- Responsywne layouty

## Testowanie

### Ręczne Testy

1. Test instalacji:
   ```bash
   python test_installation.py
   ```

2. Test podstawowy:
   - Wybierz krótki film (1-2 min)
   - Przetestuj cały workflow
   - Sprawdź jakość wyjścia

3. Test edge cases:
   - Bardzo krótki film (< 30s)
   - Długi film (> 30min)
   - Zła jakość audio
   - Różne formaty wideo

### Unit Tests (TODO)

```bash
pytest tests/
```

## Review Process

1. **Automatyczne Sprawdzenia:**
   - Code style (TODO: pre-commit hooks)
   - Linting
   - Basic tests

2. **Manualne Review:**
   - Przegląd kodu
   - Test funkcjonalności
   - Sprawdzenie dokumentacji

3. **Merge:**
   - Po zatwierdzeniu przez maintainera
   - Squash commits jeśli potrzeba

## Code of Conduct

### Nasze Zobowiązanie

- Tworzymy przyjazne i włączające środowisko
- Szanujemy różne perspektywy i doświadczenia
- Akceptujemy konstruktywną krytykę

### Niedozwolone Zachowania

- Obraźliwy język lub obrazy
- Trolling lub obraźliwe komentarze
- Harassment
- Publishing private information

### Egzekwowanie

Naruszenia można zgłaszać przez utworzenie issue lub kontakt z maintainerem.

## Pytania?

- Przeczytaj [README.md](README.md)
- Sprawdź [FAQ.md](FAQ.md)
- Sprawdź [TECHNICAL.md](TECHNICAL.md)
- Utwórz issue z pytaniem

## Licencja

Kontrybuując do tego projektu, zgadzasz się że Twoje zmiany będą licencjonowane na licencji MIT.

## Podziękowania

Dziękujemy wszystkim kontrybutorm za pomoc w rozwoju projektu! 🙏

### Top Contributors

(Lista zostanie zaktualizowana)

---

**Miłego kodowania!** 💻🎬
