"""
Edytor Słownika
Dialog do edycji niestandardowego słownika tłumaczeń
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt


class DictionaryEditor(QDialog):
    """Dialog edycji słownika tłumaczeń"""
    
    def __init__(self, dictionary: dict, parent=None):
        super().__init__(parent)
        self.dictionary = dictionary.copy()
        self.init_ui()
        self.load_dictionary()
    
    def init_ui(self):
        """Inicjalizacja interfejsu"""
        self.setWindowTitle("Edytor Słownika Tłumaczeń")
        self.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout()
        
        # Nagłówek
        header_label = QLabel("Słownik Niestandardowych Tłumaczeń")
        header_label.setStyleSheet("QLabel { font-size: 14pt; font-weight: bold; }")
        layout.addWidget(header_label)
        
        # Info
        info_label = QLabel("Wprowadź terminy angielskie i ich polskie odpowiedniki (specjalistyczne terminy tradingowe)")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Termin Angielski", "Polskie Tłumaczenie"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # Przyciski dodawania/usuwania
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Dodaj Pozycję")
        add_btn.clicked.connect(self.add_entry)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Usuń Wybraną")
        remove_btn.clicked.connect(self.remove_entry)
        button_layout.addWidget(remove_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Przyciski OK/Anuluj
        dialog_buttons = QHBoxLayout()
        
        ok_btn = QPushButton("Zapisz")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 5px; }")
        dialog_buttons.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Anuluj")
        cancel_btn.clicked.connect(self.reject)
        dialog_buttons.addWidget(cancel_btn)
        
        layout.addLayout(dialog_buttons)
        
        self.setLayout(layout)
    
    def load_dictionary(self):
        """Załaduj słownik do tabeli"""
        self.table.setRowCount(len(self.dictionary))
        
        for row, (english, polish) in enumerate(self.dictionary.items()):
            self.table.setItem(row, 0, QTableWidgetItem(english))
            self.table.setItem(row, 1, QTableWidgetItem(polish))
    
    def add_entry(self):
        """Dodaj nową pozycję"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        self.table.setItem(row, 1, QTableWidgetItem(""))
    
    def remove_entry(self):
        """Usuń wybraną pozycję"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
    
    def get_dictionary(self) -> dict:
        """Pobierz edytowany słownik
        
        Returns:
            Słownik z tłumaczeniami
        """
        dictionary = {}
        
        for row in range(self.table.rowCount()):
            english_item = self.table.item(row, 0)
            polish_item = self.table.item(row, 1)
            
            if english_item and polish_item:
                english = english_item.text().strip()
                polish = polish_item.text().strip()
                
                if english and polish:
                    dictionary[english] = polish
        
        return dictionary
    
    def accept(self):
        """Zaakceptuj i zapisz zmiany"""
        self.dictionary = self.get_dictionary()
        super().accept()
