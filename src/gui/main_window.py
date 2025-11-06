"""
Główne okno aplikacji
Windows-style GUI dla aplikacji do dubbingu
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QProgressBar, QFileDialog,
                             QTabWidget, QTextEdit, QMessageBox, QGroupBox,
                             QLineEdit, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMetaType
from PyQt5.QtGui import QFont, QIcon, QTextCursor

from src.utils.config_manager import ConfigManager
from src.core.dubbing_engine import DubbingEngine
from src.gui.dictionary_editor import DictionaryEditor
from src.gui.translation_editor import TranslationEditor
from src.gui.settings_dialog import SettingsDialog


class DubbingWorker(QThread):
    """Wątek roboczy do przetwarzania dubbingu"""
    
    progress = pyqtSignal(str, float)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, engine, video_path, output_path, custom_dict, edited_translations):
        super().__init__()
        self.engine = engine
        self.video_path = video_path
        self.output_path = output_path
        self.custom_dict = custom_dict
        self.edited_translations = edited_translations
    
    def run(self):
        """Uruchom proces dubbingu"""
        try:
            success = self.engine.process_video(
                self.video_path,
                self.output_path,
                self.custom_dict,
                self.edited_translations
            )
            
            if success:
                self.finished.emit(True, "Dubbing zakończony pomyślnie!")
            else:
                self.finished.emit(False, "Wystąpił błąd podczas dubbingu.")
                
        except Exception as e:
            self.finished.emit(False, f"Błąd: {str(e)}")


class MainWindow(QMainWindow):
    """Główne okno aplikacji"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.dubbing_engine = None
        self.worker = None
        self.video_path = None
        self.output_path = None
        self.custom_dictionary = {}
        self.edited_translations = {}
        self.transcription_segments = None
        
        self.init_ui()
        self.init_dubbing_engine()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Profesjonalna Aplikacja do Dubbingu Filmów")
        self.setGeometry(100, 100, 1000, 700)
        
        # Centralne widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Nagłówek
        header_label = QLabel("Aplikacja do Dubbingu Filmów - Trading Videos")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Sekcja wyboru plików
        file_group = QGroupBox("Wybór Plików")
        file_layout = QVBoxLayout()
        
        # Plik wejściowy
        input_layout = QHBoxLayout()
        self.input_label = QLabel("Brak wybranego pliku")
        self.input_label.setStyleSheet("QLabel { padding: 5px; border: 1px solid #ccc; }")
        input_btn = QPushButton("Wybierz Film")
        input_btn.clicked.connect(self.select_input_file)
        input_layout.addWidget(QLabel("Plik wejściowy:"))
        input_layout.addWidget(self.input_label, 1)
        input_layout.addWidget(input_btn)
        file_layout.addLayout(input_layout)
        
        # Plik wyjściowy
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Automatycznie w katalogu 'output'")
        self.output_label.setStyleSheet("QLabel { padding: 5px; border: 1px solid #ccc; }")
        output_btn = QPushButton("Wybierz Lokalizację")
        output_btn.clicked.connect(self.select_output_file)
        output_layout.addWidget(QLabel("Plik wyjściowy:"))
        output_layout.addWidget(self.output_label, 1)
        output_layout.addWidget(output_btn)
        file_layout.addLayout(output_layout)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Zakładki
        self.tabs = QTabWidget()
        
        # Zakładka 1: Główna
        main_tab = QWidget()
        main_tab_layout = QVBoxLayout()
        
        # Przyciski akcji
        action_group = QGroupBox("Akcje")
        action_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("Podgląd Transkrypcji")
        self.preview_btn.clicked.connect(self.preview_transcription)
        self.preview_btn.setEnabled(False)
        
        self.dict_btn = QPushButton("Edytuj Słownik")
        self.dict_btn.clicked.connect(self.open_dictionary_editor)
        
        self.translate_btn = QPushButton("Edytuj Tłumaczenia")
        self.translate_btn.clicked.connect(self.open_translation_editor)
        self.translate_btn.setEnabled(False)
        
        self.start_btn = QPushButton("Rozpocznij Dubbing")
        self.start_btn.clicked.connect(self.start_dubbing)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        
        action_layout.addWidget(self.preview_btn)
        action_layout.addWidget(self.dict_btn)
        action_layout.addWidget(self.translate_btn)
        action_layout.addWidget(self.start_btn)
        action_group.setLayout(action_layout)
        main_tab_layout.addWidget(action_group)
        
        # Pasek postępu
        progress_group = QGroupBox("Postęp")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_label = QLabel("Oczekiwanie...")
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_group.setLayout(progress_layout)
        main_tab_layout.addWidget(progress_group)
        
        # Log
        log_group = QGroupBox("Logi")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        main_tab_layout.addWidget(log_group)
        
        main_tab_layout.addStretch()
        main_tab.setLayout(main_tab_layout)
        
        # Zakładka 2: Ustawienia
        settings_tab = QWidget()
        settings_layout = QVBoxLayout()
        
        settings_btn = QPushButton("Otwórz Ustawienia Zaawansowane")
        settings_btn.clicked.connect(self.open_settings_dialog)
        settings_layout.addWidget(settings_btn)
        
        # Szybkie ustawienia
        quick_settings_group = QGroupBox("Szybkie Ustawienia")
        quick_layout = QVBoxLayout()
        
        # Model Whisper
        whisper_layout = QHBoxLayout()
        whisper_layout.addWidget(QLabel("Model Whisper:"))
        self.whisper_combo = QComboBox()
        self.whisper_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.whisper_combo.setCurrentText(self.config_manager.get('whisper.model_size', 'medium'))
        whisper_layout.addWidget(self.whisper_combo)
        whisper_layout.addStretch()
        quick_layout.addLayout(whisper_layout)
        
        # CUDA
        cuda_layout = QHBoxLayout()
        self.cuda_checkbox = QCheckBox("Użyj CUDA (GPU)")
        self.cuda_checkbox.setChecked(self.config_manager.get('whisper.device', 'cuda') == 'cuda')
        cuda_layout.addWidget(self.cuda_checkbox)
        cuda_layout.addStretch()
        quick_layout.addLayout(cuda_layout)
        
        # Dopasowanie tempo
        tempo_layout = QHBoxLayout()
        self.tempo_checkbox = QCheckBox("Włącz dopasowanie tempa wideo")
        self.tempo_checkbox.setChecked(self.config_manager.get('video.tempo_adjustment_enabled', True))
        tempo_layout.addWidget(self.tempo_checkbox)
        tempo_layout.addStretch()
        quick_layout.addLayout(tempo_layout)
        
        # Klatki kluczowe
        keyframe_layout = QHBoxLayout()
        self.keyframe_checkbox = QCheckBox("Dodaj klatki kluczowe")
        self.keyframe_checkbox.setChecked(self.config_manager.get('video.add_keyframes', True))
        keyframe_layout.addWidget(self.keyframe_checkbox)
        keyframe_layout.addStretch()
        quick_layout.addLayout(keyframe_layout)
        
        # Zapisz ustawienia
        save_settings_btn = QPushButton("Zapisz Ustawienia")
        save_settings_btn.clicked.connect(self.save_quick_settings)
        quick_layout.addWidget(save_settings_btn)
        
        quick_settings_group.setLayout(quick_layout)
        settings_layout.addWidget(quick_settings_group)
        
        settings_layout.addStretch()
        settings_tab.setLayout(settings_layout)
        
        # Dodaj zakładki
        self.tabs.addTab(main_tab, "Główna")
        self.tabs.addTab(settings_tab, "Ustawienia")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Gotowy")
        
        self.log("Aplikacja uruchomiona. Wybierz film do przetworzenia.")
    
    def init_dubbing_engine(self):
        """Inicjalizacja silnika dubbingu"""
        try:
            config = self.config_manager.config
            self.dubbing_engine = DubbingEngine(config, self.update_progress)
            self.custom_dictionary = self.config_manager.load_custom_dictionary()
            self.log("Silnik dubbingu zainicjalizowany.")
        except Exception as e:
            self.log(f"Błąd inicjalizacji silnika: {e}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się zainicjalizować silnika dubbingu: {e}")
    
    def select_input_file(self):
        """Wybór pliku wejściowego"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz Film",
            "",
            "Pliki Wideo (*.mp4 *.avi *.mkv *.mov);;Wszystkie Pliki (*.*)"
        )
        
        if file_path:
            self.video_path = file_path
            self.input_label.setText(os.path.basename(file_path))
            self.log(f"Wybrano plik: {file_path}")
            
            # Automatycznie ustaw ścieżkę wyjściową
            if not self.output_path:
                output_dir = self.config_manager.get('paths.output_dir', 'output')
                os.makedirs(output_dir, exist_ok=True)
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                self.output_path = os.path.join(output_dir, f"{base_name}_dubbed.mp4")
                self.output_label.setText(os.path.basename(self.output_path))
            
            self.preview_btn.setEnabled(True)
            self.start_btn.setEnabled(True)
    
    def select_output_file(self):
        """Wybór pliku wyjściowego"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Wybierz Lokalizację Zapisu",
            self.output_path if self.output_path else "output.mp4",
            "Pliki MP4 (*.mp4);;Wszystkie Pliki (*.*)"
        )
        
        if file_path:
            self.output_path = file_path
            self.output_label.setText(os.path.basename(file_path))
            self.log(f"Ścieżka wyjściowa: {file_path}")
    
    def preview_transcription(self):
        """Podgląd transkrypcji"""
        if not self.video_path:
            QMessageBox.warning(self, "Ostrzeżenie", "Najpierw wybierz film!")
            return
        
        self.log("Pobieranie podglądu transkrypcji...")
        self.progress_label.setText("Transkrypcja w toku...")
        self.progress_bar.setValue(0)
        
        try:
            segments = self.dubbing_engine.get_transcription_preview(self.video_path)
            
            if segments:
                self.transcription_segments = segments
                self.translate_btn.setEnabled(True)
                self.log(f"Transkrypcja zakończona. Wykryto {len(segments)} segmentów.")
                
                # Pokaż podgląd
                preview_text = "Podgląd transkrypcji:\n\n"
                for i, seg in enumerate(segments[:10]):  # Pokaż tylko pierwsze 10
                    preview_text += f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}\n"
                
                if len(segments) > 10:
                    preview_text += f"\n... i {len(segments) - 10} więcej segmentów"
                
                QMessageBox.information(self, "Podgląd Transkrypcji", preview_text)
                self.progress_bar.setValue(100)
            else:
                self.log("Błąd podczas transkrypcji.")
                QMessageBox.critical(self, "Błąd", "Nie udało się przetworzyć transkrypcji.")
                
        except Exception as e:
            self.log(f"Błąd: {e}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {e}")
    
    def open_dictionary_editor(self):
        """Otwórz edytor słownika"""
        dialog = DictionaryEditor(self.custom_dictionary, self)
        if dialog.exec_():
            self.custom_dictionary = dialog.get_dictionary()
            self.config_manager.save_custom_dictionary(self.custom_dictionary)
            self.log("Słownik zaktualizowany.")
    
    def open_translation_editor(self):
        """Otwórz edytor tłumaczeń"""
        if not self.transcription_segments:
            QMessageBox.warning(self, "Ostrzeżenie", "Najpierw wykonaj podgląd transkrypcji!")
            return
        
        # Przetłumacz segmenty
        self.dubbing_engine.translation.set_custom_dictionary(self.custom_dictionary)
        translated_segments = self.dubbing_engine.translation.translate_segments(
            self.transcription_segments
        )
        
        dialog = TranslationEditor(translated_segments, self)
        if dialog.exec_():
            self.edited_translations = dialog.get_edited_translations()
            self.log(f"Edytowano {len(self.edited_translations)} tłumaczeń.")
    
    def open_settings_dialog(self):
        """Otwórz dialog ustawień zaawansowanych"""
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec_():
            self.config_manager.save_config()
            self.log("Ustawienia zapisane.")
            # Reinicjalizuj silnik z nowymi ustawieniami
            self.init_dubbing_engine()
    
    def save_quick_settings(self):
        """Zapisz szybkie ustawienia"""
        self.config_manager.set('whisper.model_size', self.whisper_combo.currentText())
        self.config_manager.set('whisper.device', 'cuda' if self.cuda_checkbox.isChecked() else 'cpu')
        self.config_manager.set('video.tempo_adjustment_enabled', self.tempo_checkbox.isChecked())
        self.config_manager.set('video.add_keyframes', self.keyframe_checkbox.isChecked())
        
        if self.config_manager.save_config():
            self.log("Ustawienia zapisane pomyślnie.")
            QMessageBox.information(self, "Sukces", "Ustawienia zapisane!")
            # Reinicjalizuj silnik
            self.init_dubbing_engine()
        else:
            QMessageBox.critical(self, "Błąd", "Nie udało się zapisać ustawień.")
    
    def start_dubbing(self):
        """Rozpocznij proces dubbingu"""
        if not self.video_path or not self.output_path:
            QMessageBox.warning(self, "Ostrzeżenie", "Wybierz pliki wejściowe i wyjściowe!")
            return
        
        # Potwierdź rozpoczęcie
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy rozpocząć proces dubbingu? Może to potrwać kilka minut.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Wyłącz przyciski
        self.start_btn.setEnabled(False)
        self.preview_btn.setEnabled(False)
        
        # Utwórz i uruchom wątek roboczy
        self.worker = DubbingWorker(
            self.dubbing_engine,
            self.video_path,
            self.output_path,
            self.custom_dictionary,
            self.edited_translations
        )
        
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.dubbing_finished)
        self.worker.start()
        
        self.log("Rozpoczęto proces dubbingu...")
    
    def update_progress(self, message: str, progress: float):
        """Aktualizuj postęp
        
        Args:
            message: Wiadomość o postępie
            progress: Procent (0-100)
        """
        self.progress_label.setText(message)
        self.progress_bar.setValue(int(progress))
        self.log(f"[{progress:.1f}%] {message}")
    
    def dubbing_finished(self, success: bool, message: str):
        """Obsłuż zakończenie dubbingu
        
        Args:
            success: Czy proces się powiódł
            message: Wiadomość o wyniku
        """
        self.start_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        if success:
            self.log("Dubbing zakończony pomyślnie!")
            QMessageBox.information(self, "Sukces", f"{message}\n\nPlik zapisany: {self.output_path}")
            self.progress_bar.setValue(100)
        else:
            self.log(f"Błąd podczas dubbingu: {message}")
            QMessageBox.critical(self, "Błąd", message)
            self.progress_bar.setValue(0)
    
    def log(self, message: str):
        """Dodaj wiadomość do logu (thread-safe)
        
        Args:
            message: Wiadomość do wyświetlenia
        """
        # Używamy invokeMethod aby zapewnić, że append jest wywołany w głównym wątku GUI
        from PyQt5.QtCore import QMetaObject, Qt as QtCore_Qt
        QMetaObject.invokeMethod(self.log_text, "append", QtCore_Qt.QueuedConnection, message)
        self.statusBar().showMessage(message)
    
    def closeEvent(self, event):
        """Obsługa zamykania okna - bezpiecznie zakończ wątek roboczy
        
        Args:
            event: Zdarzenie zamknięcia
        """
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, 
                'Potwierdzenie',
                'Przetwarzanie jest w toku. Czy na pewno chcesz zamknąć aplikację?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.terminate()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
