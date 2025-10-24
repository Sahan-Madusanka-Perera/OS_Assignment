from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class ResultsPanel(QWidget):
    """Panel to display simulation statistics"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Simulation Results")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        self.stats_layout = QGridLayout()
        layout.addLayout(self.stats_layout)
        
        self.labels = {}
        stats = ['Algorithm', 'Page Faults', 'Hits', 'Hit Ratio', 'Fault Ratio']
        
        for i, stat in enumerate(stats):
            label = QLabel(f"{stat}:")
            label.setStyleSheet("font-weight: bold;")
            value = QLabel("--")
            
            self.stats_layout.addWidget(label, i, 0)
            self.stats_layout.addWidget(value, i, 1)
            self.labels[stat] = value
    
    def display_statistics(self, results):
        """Update the statistics display with simulation results"""
        self.labels['Algorithm'].setText(results.get('algorithm', '--'))
        self.labels['Page Faults'].setText(str(results.get('page_faults', 0)))
        self.labels['Hits'].setText(str(results.get('hits', 0)))
        self.labels['Hit Ratio'].setText(f"{results.get('hit_ratio', 0):.2%}")
        self.labels['Fault Ratio'].setText(f"{results.get('fault_ratio', 0):.2%}")
