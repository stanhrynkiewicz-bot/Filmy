"""
Edytor Tłumaczeń
Dialog do edycji przetłumaczonych tekstów przed generowaniem lektora
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QTextEdit,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt


class TranslationEditor(QDialog):
    """Dialog edycji tłumaczeń"""
    
    def __init__(self, segments: list, parent=None):
        super().__init__(parent)
        self.segments = segments
        self.edited_translations = {}
        self.init_ui()
        self.load_segments()
    
    def init_ui(self):
        """Inicjalizacja interfejsu"""
        self.setWindowTitle("Edytor Tłumaczeń")
        self.setGeometry(150, 150, 900, 600)
        
        layout = QVBoxLayout()
        
        # Nagłówek
        header_label = QLabel("Edycja Tłumaczeń")
        header_label.setStyleSheet("QLabel { font-size: 14pt; font-weight: bold; }")
        layout.addWidget(header_label)
        
        # Info
        info_label = QLabel("Kliknij dwukrotnie na tłumaczenie, aby je edytować. Zmiany będą użyte przy generowaniu lektora.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Czas", "Tekst Oryginalny", "Tłumaczenie", "Status"])
        
        # Proporcje kolumn
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.table.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.table)
        
        # Statystyki
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Segmentów: 0 | Edytowanych: 0")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Resetuj Wszystkie")
        reset_btn.clicked.connect(self.reset_all)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        ok_btn = QPushButton("Zapisz Zmiany")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 5px; }")
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Anuluj")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_segments(self):
        """Załaduj segmenty do tabeli"""
        self.table.setRowCount(len(self.segments))
        
        for row, seg in enumerate(self.segments):
            # Czas
            time_str = f"{seg['start']:.1f}s - {seg['end']:.1f}s"
            time_item = QTableWidgetItem(time_str)
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, time_item)
            
            # Tekst oryginalny
            original_item = QTableWidgetItem(seg['text'])
            original_item.setFlags(original_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, original_item)
            
            # Tłumaczenie (edytowalne)
            translation = seg.get('translated_text', '')
            translation_item = QTableWidgetItem(translation)
            self.table.setItem(row, 2, translation_item)
            
            # Status
            status_item = QTableWidgetItem("Oryginalne")
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, status_item)
        
        self.update_stats()
    
    def on_item_changed(self, item):
        """Obsłuż zmianę elementu
        
        Args:
            item: Zmieniony element
        """
        if item.column() == 2:  # Kolumna tłumaczeń
            row = item.row()
            new_translation = item.text()
            original_translation = self.segments[row].get('translated_text', '')
            
            if new_translation != original_translation:
                # Oznacz jako edytowane
                self.edited_translations[row] = new_translation
                status_item = self.table.item(row, 3)
                if status_item:
                    status_item.setText("Edytowane")
                    status_item.setForeground(Qt.blue)
            else:
                # Usunąć z edytowanych jeśli przywrócono oryginał
                if row in self.edited_translations:
                    del self.edited_translations[row]
                    status_item = self.table.item(row, 3)
                    if status_item:
                        status_item.setText("Oryginalne")
                        status_item.setForeground(Qt.black)
            
            self.update_stats()
    
    def update_stats(self):
        """Aktualizuj statystyki"""
        total = len(self.segments)
        edited = len(self.edited_translations)
        self.stats_label.setText(f"Segmentów: {total} | Edytowanych: {edited}")
    
    def reset_all(self):
        """Resetuj wszystkie edycje"""
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz zresetować wszystkie edycje?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.edited_translations.clear()
            self.load_segments()
    
    def get_edited_translations(self) -> dict:
        """Pobierz edytowane tłumaczenia
        
        Returns:
            Słownik {indeks_segmentu: nowy_tekst}
        """
        return self.edited_translations.copy()
    
    def accept(self):
        """Zaakceptuj zmiany"""
        if self.edited_translations:
            reply = QMessageBox.question(
                self,
                "Potwierdzenie",
                f"Zapisać {len(self.edited_translations)} edytowanych tłumaczeń?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        super().accept()
