#!/usr/bin/env python3
"""
Skrypt testowy do weryfikacji instalacji
Sprawdza czy wszystkie wymagane komponenty są dostępne
"""

import sys


def test_python_version():
    """Test wersji Pythona"""
    print("✓ Sprawdzanie wersji Pythona...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ✗ BŁĄD: Wymagany Python 3.8 lub nowszy!")
        return False
    print("  ✓ Wersja Python OK")
    return True


def test_imports():
    """Test importów bibliotek"""
    print("\n✓ Sprawdzanie bibliotek...")
    
    libraries = [
        ("torch", "PyTorch"),
        ("whisper", "OpenAI Whisper"),
        ("TTS", "Coqui TTS"),
        ("PyQt5", "PyQt5"),
        ("moviepy.editor", "MoviePy"),
        ("pydub", "Pydub"),
        ("deep_translator", "Deep Translator"),
        ("yaml", "PyYAML"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
    ]
    
    all_ok = True
    for module_name, display_name in libraries:
        try:
            __import__(module_name)
            print(f"  ✓ {display_name}")
        except ImportError as e:
            print(f"  ✗ {display_name} - BRAK!")
            all_ok = False
    
    return all_ok


def test_cuda():
    """Test dostępności CUDA"""
    print("\n✓ Sprawdzanie CUDA...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  ✓ CUDA dostępna")
            print(f"  ✓ Urządzenie: {torch.cuda.get_device_name(0)}")
            print(f"  ✓ CUDA wersja: {torch.version.cuda}")
            return True
        else:
            print("  ! CUDA niedostępna - będzie używany CPU (wolniejsze)")
            return True  # Nie jest błędem, tylko ostrzeżeniem
    except Exception as e:
        print(f"  ✗ Błąd sprawdzania CUDA: {e}")
        return False


def test_ffmpeg():
    """Test FFmpeg"""
    print("\n✓ Sprawdzanie FFmpeg...")
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✓ FFmpeg zainstalowany: {version_line}")
            return True
        else:
            print("  ✗ FFmpeg nie działa poprawnie")
            return False
    except FileNotFoundError:
        print("  ✗ FFmpeg nie znaleziony w PATH!")
        print("  Zainstaluj FFmpeg i dodaj do PATH")
        return False
    except Exception as e:
        print(f"  ✗ Błąd sprawdzania FFmpeg: {e}")
        return False


def test_directories():
    """Test struktury katalogów"""
    print("\n✓ Sprawdzanie struktury katalogów...")
    import os
    
    dirs = ['src', 'src/core', 'src/gui', 'src/utils', 'models']
    all_ok = True
    
    for dir_path in dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ - BRAK!")
            all_ok = False
    
    return all_ok


def test_config():
    """Test konfiguracji"""
    print("\n✓ Sprawdzanie konfiguracji...")
    import os
    
    if os.path.exists('config.yaml'):
        print("  ✓ config.yaml istnieje")
        return True
    elif os.path.exists('config.yaml.template'):
        print("  ! config.yaml nie istnieje, ale jest template")
        print("  Skopiuj config.yaml.template do config.yaml")
        return True
    else:
        print("  ✗ Brak plików konfiguracyjnych!")
        return False


def test_dictionary():
    """Test słownika"""
    print("\n✓ Sprawdzanie słownika...")
    import os
    import json
    
    if os.path.exists('custom_dictionary.json'):
        try:
            with open('custom_dictionary.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  ✓ Słownik załadowany ({len(data)} kategorii)")
            return True
        except Exception as e:
            print(f"  ✗ Błąd wczytywania słownika: {e}")
            return False
    else:
        print("  ! Brak słownika (zostanie utworzony przy pierwszym uruchomieniu)")
        return True


def test_application_imports():
    """Test importów aplikacji"""
    print("\n✓ Sprawdzanie modułów aplikacji...")
    
    modules = [
        "src.utils.config_manager",
        "src.core.transcription",
        "src.core.translation",
        "src.core.tts",
        "src.core.video_processor",
        "src.core.dubbing_engine",
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module} - BŁĄD: {e}")
            all_ok = False
    
    return all_ok


def main():
    """Główna funkcja testowa"""
    print("=" * 60)
    print("Test Instalacji - Aplikacja do Dubbingu Filmów")
    print("=" * 60)
    
    tests = [
        ("Wersja Python", test_python_version),
        ("Biblioteki", test_imports),
        ("CUDA", test_cuda),
        ("FFmpeg", test_ffmpeg),
        ("Struktura katalogów", test_directories),
        ("Konfiguracja", test_config),
        ("Słownik", test_dictionary),
        ("Moduły aplikacji", test_application_imports),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Nieoczekiwany błąd w teście '{name}': {e}")
            results.append((name, False))
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("PODSUMOWANIE")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ OK" if result else "✗ BŁĄD"
        print(f"{status:8} {name}")
    
    print("-" * 60)
    print(f"Wynik: {passed}/{total} testów zaliczonych")
    
    if passed == total:
        print("\n✓ Wszystkie testy zaliczone!")
        print("✓ Aplikacja jest gotowa do użycia.")
        print("\nUruchom aplikację: python dubbing_app.py")
        return 0
    else:
        print(f"\n✗ {total - passed} testów nie powiodło się")
        print("✗ Napraw błędy przed uruchomieniem aplikacji")
        return 1


if __name__ == "__main__":
    sys.exit(main())
