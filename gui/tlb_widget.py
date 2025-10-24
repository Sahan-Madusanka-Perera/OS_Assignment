from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QGridLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class TLBVisualizationWidget(QWidget):
    """Widget to visualize TLB performance"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        stats_group = QGroupBox("TLB Statistics")
        stats_layout = QGridLayout()
        
        self.tlb_labels = {}
        stats = ['Hits', 'Misses', 'Hit Ratio', 'Size', 'Capacity']
        
        for i, stat in enumerate(stats):
            label = QLabel(f"{stat}:")
            label.setStyleSheet("font-weight: bold;")
            value = QLabel("--")
            
            stats_layout.addWidget(label, i, 0)
            stats_layout.addWidget(value, i, 1)
            self.tlb_labels[stat] = value
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)
    
    def display_tlb_stats(self, tlb_stats):
        """Display TLB statistics"""
        if not tlb_stats:
            return
        
        self.tlb_labels['Hits'].setText(str(tlb_stats['hits']))
        self.tlb_labels['Misses'].setText(str(tlb_stats['misses']))
        self.tlb_labels['Hit Ratio'].setText(f"{tlb_stats['hit_ratio']:.2%}")
        self.tlb_labels['Size'].setText(str(tlb_stats['size']))
        self.tlb_labels['Capacity'].setText(str(tlb_stats['capacity']))
        
        self.display_chart(tlb_stats)
    
    def display_chart(self, tlb_stats):
        """Display TLB performance chart"""
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        categories = ['TLB Hits', 'TLB Misses']
        values = [tlb_stats['hits'], tlb_stats['misses']]
        colors = ['#51cf66', '#ff6b6b']
        
        wedges, texts, autotexts = ax.pie(values, labels=categories, colors=colors,
                                           autopct='%1.1f%%', startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(f"TLB Performance - Hit Ratio: {tlb_stats['hit_ratio']:.2%}")
        
        self.canvas.draw()
