from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QGridLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class WorkingSetWidget(QWidget):
    """Widget to visualize working set and detect thrashing"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        stats_group = QGroupBox("Working Set Analysis")
        stats_layout = QGridLayout()
        
        self.ws_labels = {}
        stats = ['Working Set Size', 'Fault Rate', 'Status']
        
        for i, stat in enumerate(stats):
            label = QLabel(f"{stat}:")
            label.setStyleSheet("font-weight: bold;")
            value = QLabel("--")
            
            stats_layout.addWidget(label, i, 0)
            stats_layout.addWidget(value, i, 1)
            self.ws_labels[stat] = value
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)
        
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_label.hide()
        layout.addWidget(self.warning_label)
    
    def display_working_set_stats(self, ws_stats, num_frames):
        """Display working set statistics"""
        if not ws_stats:
            return
        
        self.ws_labels['Working Set Size'].setText(str(ws_stats['current_working_set']))
        self.ws_labels['Fault Rate'].setText(f"{ws_stats['fault_rate']:.2%}")
        
        if ws_stats['is_thrashing']:
            status = "⚠️ THRASHING DETECTED!"
            self.ws_labels['Status'].setText(status)
            self.ws_labels['Status'].setStyleSheet("color: red; font-weight: bold;")
            
            self.warning_label.setText(
                f"Warning: System is thrashing!\n"
                f"Working set ({ws_stats['current_working_set']}) > Frames ({num_frames})\n"
                f"Recommendation: Increase frames or reduce working set"
            )
            self.warning_label.setStyleSheet(
                "background-color: #fff3cd; color: #856404; "
                "border: 2px solid #ffc107; border-radius: 5px; "
                "font-size: 14px; font-weight: bold; padding: 10px;"
            )
            self.warning_label.show()
        else:
            status = "✓ Normal Operation"
            self.ws_labels['Status'].setText(status)
            self.ws_labels['Status'].setStyleSheet("color: green; font-weight: bold;")
            self.warning_label.hide()
        
        self.display_chart(ws_stats, num_frames)
    
    def display_chart(self, ws_stats, num_frames):
        """Display working set size over time"""
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        history = ws_stats['working_set_history']
        if not history:
            return
        
        steps = list(range(1, len(history) + 1))
        
        ax.plot(steps, history, 'b-', linewidth=2, label='Working Set Size')
        ax.axhline(y=num_frames, color='r', linestyle='--', linewidth=2, label=f'Available Frames ({num_frames})')
        
        if ws_stats['is_thrashing']:
            ax.fill_between(steps, history, num_frames, 
                           where=[h > num_frames for h in history],
                           color='red', alpha=0.3, label='Thrashing Region')
        
        ax.set_xlabel('Access Step')
        ax.set_ylabel('Working Set Size')
        ax.set_title('Working Set Size Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        self.canvas.draw()
