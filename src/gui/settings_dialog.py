"""
Dialog Ustawień Zaawansowanych
Umożliwia szczegółową konfigurację aplikacji
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QCheckBox, QSpinBox,
                             QDoubleSpinBox, QGroupBox, QTabWidget, QWidget,
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    """Dialog ustawień zaawansowanych"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Inicjalizacja interfejsu"""
        self.setWindowTitle("Ustawienia Zaawansowane")
        self.setGeometry(150, 150, 600, 500)
        
        layout = QVBoxLayout()
        
        # Zakładki
        tabs = QTabWidget()
        
        # Zakładka Whisper
        whisper_tab = self.create_whisper_tab()
        tabs.addTab(whisper_tab, "Whisper")
        
        # Zakładka Tłumaczenie
        translation_tab = self.create_translation_tab()
        tabs.addTab(translation_tab, "Tłumaczenie")
        
        # Zakładka TTS
        tts_tab = self.create_tts_tab()
        tabs.addTab(tts_tab, "TTS")
        
        # Zakładka Wideo
        video_tab = self.create_video_tab()
        tabs.addTab(video_tab, "Wideo")
        
        # Zakładka Audio
        audio_tab = self.create_audio_tab()
        tabs.addTab(audio_tab, "Audio")
        
        # Zakładka Ścieżki
        paths_tab = self.create_paths_tab()
        tabs.addTab(paths_tab, "Ścieżki")
        
        layout.addWidget(tabs)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Przywróć Domyślne")
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("Zapisz")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 5px; }")
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Anuluj")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_whisper_tab(self) -> QWidget:
        """Utwórz zakładkę ustawień Whisper"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Ustawienia Whisper")
        group_layout = QVBoxLayout()
        
        # Model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Rozmiar modelu:"))
        self.whisper_model = QComboBox()
        self.whisper_model.addItems(["tiny", "base", "small", "medium", "large"])
        model_layout.addWidget(self.whisper_model)
        model_layout.addStretch()
        group_layout.addLayout(model_layout)
        
        # Urządzenie
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Urządzenie:"))
        self.whisper_device = QComboBox()
        self.whisper_device.addItems(["cuda", "cpu"])
        device_layout.addWidget(self.whisper_device)
        device_layout.addStretch()
        group_layout.addLayout(device_layout)
        
        # Język
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Język źródłowy:"))
        self.whisper_lang = QLineEdit()
        lang_layout.addWidget(self.whisper_lang)
        group_layout.addLayout(lang_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_translation_tab(self) -> QWidget:
        """Utwórz zakładkę ustawień tłumaczenia"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Ustawienia Tłumaczenia")
        group_layout = QVBoxLayout()
        
        # Język źródłowy
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Język źródłowy:"))
        self.trans_source = QLineEdit()
        source_layout.addWidget(self.trans_source)
        group_layout.addLayout(source_layout)
        
        # Język docelowy
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Język docelowy:"))
        self.trans_target = QLineEdit()
        target_layout.addWidget(self.trans_target)
        group_layout.addLayout(target_layout)
        
        # Serwis
        service_layout = QHBoxLayout()
        service_layout.addWidget(QLabel("Serwis tłumaczenia:"))
        self.trans_service = QComboBox()
        self.trans_service.addItems(["google"])
        service_layout.addWidget(self.trans_service)
        service_layout.addStretch()
        group_layout.addLayout(service_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_tts_tab(self) -> QWidget:
        """Utwórz zakładkę ustawień TTS"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Ustawienia TTS")
        group_layout = QVBoxLayout()
        
        # Model
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Nazwa modelu:"))
        self.tts_model = QLineEdit()
        model_layout.addWidget(self.tts_model)
        group_layout.addLayout(model_layout)
        
        # Język
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Język:"))
        self.tts_lang = QLineEdit()
        lang_layout.addWidget(self.tts_lang)
        group_layout.addLayout(lang_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_video_tab(self) -> QWidget:
        """Utwórz zakładkę ustawień wideo"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Ustawienia Przetwarzania Wideo")
        group_layout = QVBoxLayout()
        
        # Próg ciszy
        silence_layout = QHBoxLayout()
        silence_layout.addWidget(QLabel("Próg ciszy (s):"))
        self.video_silence = QDoubleSpinBox()
        self.video_silence.setRange(0.1, 5.0)
        self.video_silence.setSingleStep(0.1)
        self.video_silence.setDecimals(1)
        silence_layout.addWidget(self.video_silence)
        silence_layout.addStretch()
        group_layout.addLayout(silence_layout)
        
        # Min długość segmentu
        min_dur_layout = QHBoxLayout()
        min_dur_layout.addWidget(QLabel("Min. długość segmentu (s):"))
        self.video_min_dur = QDoubleSpinBox()
        self.video_min_dur.setRange(0.5, 10.0)
        self.video_min_dur.setSingleStep(0.5)
        self.video_min_dur.setDecimals(1)
        min_dur_layout.addWidget(self.video_min_dur)
        min_dur_layout.addStretch()
        group_layout.addLayout(min_dur_layout)
        
        # Max długość segmentu
        max_dur_layout = QHBoxLayout()
        max_dur_layout.addWidget(QLabel("Max. długość segmentu (s):"))
        self.video_max_dur = QDoubleSpinBox()
        self.video_max_dur.setRange(10.0, 120.0)
        self.video_max_dur.setSingleStep(5.0)
        self.video_max_dur.setDecimals(1)
        max_dur_layout.addWidget(self.video_max_dur)
        max_dur_layout.addStretch()
        group_layout.addLayout(max_dur_layout)
        
        # Dopasowanie tempo
        self.video_tempo = QCheckBox("Włącz dopasowanie tempa wideo")
        group_layout.addWidget(self.video_tempo)
        
        # Klatki kluczowe
        self.video_keyframes = QCheckBox("Dodawaj klatki kluczowe")
        group_layout.addWidget(self.video_keyframes)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_audio_tab(self) -> QWidget:
        """Utwórz zakładkę ustawień audio"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Ustawienia Audio")
        group_layout = QVBoxLayout()
        
        # Sample rate
        sr_layout = QHBoxLayout()
        sr_layout.addWidget(QLabel("Sample rate (Hz):"))
        self.audio_sr = QSpinBox()
        self.audio_sr.setRange(8000, 48000)
        self.audio_sr.setSingleStep(1000)
        sr_layout.addWidget(self.audio_sr)
        sr_layout.addStretch()
        group_layout.addLayout(sr_layout)
        
        # Próg ciszy
        thresh_layout = QHBoxLayout()
        thresh_layout.addWidget(QLabel("Próg ciszy (dB):"))
        self.audio_silence = QSpinBox()
        self.audio_silence.setRange(-80, 0)
        self.audio_silence.setSingleStep(5)
        thresh_layout.addWidget(self.audio_silence)
        thresh_layout.addStretch()
        group_layout.addLayout(thresh_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_paths_tab(self) -> QWidget:
        """Utwórz zakładkę ścieżek"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        group = QGroupBox("Katalogi")
        group_layout = QVBoxLayout()
        
        # Temp
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Katalog tymczasowy:"))
        self.path_temp = QLineEdit()
        temp_layout.addWidget(self.path_temp)
        group_layout.addLayout(temp_layout)
        
        # Output
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Katalog wyjściowy:"))
        self.path_output = QLineEdit()
        output_layout.addWidget(self.path_output)
        group_layout.addLayout(output_layout)
        
        # Cache
        cache_layout = QHBoxLayout()
        cache_layout.addWidget(QLabel("Katalog cache:"))
        self.path_cache = QLineEdit()
        cache_layout.addWidget(self.path_cache)
        group_layout.addLayout(cache_layout)
        
        # Models
        models_layout = QHBoxLayout()
        models_layout.addWidget(QLabel("Katalog modeli:"))
        self.path_models = QLineEdit()
        models_layout.addWidget(self.path_models)
        group_layout.addLayout(models_layout)
        
        # Dictionary
        dict_layout = QHBoxLayout()
        dict_layout.addWidget(QLabel("Plik słownika:"))
        self.path_dict = QLineEdit()
        dict_layout.addWidget(self.path_dict)
        group_layout.addLayout(dict_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def load_settings(self):
        """Wczytaj ustawienia z config managera"""
        # Whisper
        self.whisper_model.setCurrentText(self.config_manager.get('whisper.model_size', 'medium'))
        self.whisper_device.setCurrentText(self.config_manager.get('whisper.device', 'cuda'))
        self.whisper_lang.setText(self.config_manager.get('whisper.language', 'en'))
        
        # Translation
        self.trans_source.setText(self.config_manager.get('translation.source_lang', 'en'))
        self.trans_target.setText(self.config_manager.get('translation.target_lang', 'pl'))
        self.trans_service.setCurrentText(self.config_manager.get('translation.service', 'google'))
        
        # TTS
        self.tts_model.setText(self.config_manager.get('tts.model_name', 'tts_models/pl/mai_female/vits'))
        self.tts_lang.setText(self.config_manager.get('tts.language', 'pl'))
        
        # Video
        self.video_silence.setValue(self.config_manager.get('video.silence_threshold', 0.4))
        self.video_min_dur.setValue(self.config_manager.get('video.min_segment_duration', 1.0))
        self.video_max_dur.setValue(self.config_manager.get('video.max_segment_duration', 30.0))
        self.video_tempo.setChecked(self.config_manager.get('video.tempo_adjustment_enabled', True))
        self.video_keyframes.setChecked(self.config_manager.get('video.add_keyframes', True))
        
        # Audio
        self.audio_sr.setValue(self.config_manager.get('audio.sample_rate', 16000))
        self.audio_silence.setValue(self.config_manager.get('audio.silence_threshold_db', -40))
        
        # Paths
        self.path_temp.setText(self.config_manager.get('paths.temp_dir', 'temp_segments'))
        self.path_output.setText(self.config_manager.get('paths.output_dir', 'output'))
        self.path_cache.setText(self.config_manager.get('paths.cache_dir', 'cache'))
        self.path_models.setText(self.config_manager.get('paths.models_dir', 'models'))
        self.path_dict.setText(self.config_manager.get('paths.dictionary_file', 'custom_dictionary.json'))
    
    def save_settings(self):
        """Zapisz ustawienia do config managera"""
        # Whisper
        self.config_manager.set('whisper.model_size', self.whisper_model.currentText())
        self.config_manager.set('whisper.device', self.whisper_device.currentText())
        self.config_manager.set('whisper.language', self.whisper_lang.text())
        
        # Translation
        self.config_manager.set('translation.source_lang', self.trans_source.text())
        self.config_manager.set('translation.target_lang', self.trans_target.text())
        self.config_manager.set('translation.service', self.trans_service.currentText())
        
        # TTS
        self.config_manager.set('tts.model_name', self.tts_model.text())
        self.config_manager.set('tts.language', self.tts_lang.text())
        
        # Video
        self.config_manager.set('video.silence_threshold', self.video_silence.value())
        self.config_manager.set('video.min_segment_duration', self.video_min_dur.value())
        self.config_manager.set('video.max_segment_duration', self.video_max_dur.value())
        self.config_manager.set('video.tempo_adjustment_enabled', self.video_tempo.isChecked())
        self.config_manager.set('video.add_keyframes', self.video_keyframes.isChecked())
        
        # Audio
        self.config_manager.set('audio.sample_rate', self.audio_sr.value())
        self.config_manager.set('audio.silence_threshold_db', self.audio_silence.value())
        
        # Paths
        self.config_manager.set('paths.temp_dir', self.path_temp.text())
        self.config_manager.set('paths.output_dir', self.path_output.text())
        self.config_manager.set('paths.cache_dir', self.path_cache.text())
        self.config_manager.set('paths.models_dir', self.path_models.text())
        self.config_manager.set('paths.dictionary_file', self.path_dict.text())
        
        self.accept()
    
    def reset_to_defaults(self):
        """Przywróć domyślne ustawienia"""
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno przywrócić domyślne ustawienia?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config_manager.config = self.config_manager._get_default_config()
            self.load_settings()
