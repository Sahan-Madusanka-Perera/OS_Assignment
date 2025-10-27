from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MLPredictionWidget(QWidget):
    """Widget to visualize ML prediction performance"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Machine Learning Prediction Analysis")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("Uses pattern recognition to predict and prefetch pages before they're needed")
        desc.setStyleSheet("font-size: 11px; color: #666; font-style: italic;")
        layout.addWidget(desc)
        
        stats_layout = QHBoxLayout()
        
        self.accuracy_label = QLabel()
        self.accuracy_label.setStyleSheet(
            "font-size: 14px; padding: 15px; background-color: #e3f2fd; "
            "border: 2px solid #2196f3; border-radius: 5px; font-weight: bold;"
        )
        stats_layout.addWidget(self.accuracy_label)
        
        self.prefetch_label = QLabel()
        self.prefetch_label.setStyleSheet(
            "font-size: 14px; padding: 15px; background-color: #f3e5f5; "
            "border: 2px solid #9c27b0; border-radius: 5px; font-weight: bold;"
        )
        stats_layout.addWidget(self.prefetch_label)
        
        layout.addLayout(stats_layout)
        
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        charts_layout = QHBoxLayout()
        
        self.accuracy_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.accuracy_canvas)
        
        self.benefit_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        charts_layout.addWidget(self.benefit_canvas)
        
        layout.addLayout(charts_layout)
    
    def display_ml_comparison(self, base_results, ml_results):
        """Display comparison between base and ML-enhanced algorithms"""
        ml_stats = ml_results.get('ml_prediction_stats', {})
        
        accuracy = ml_stats.get('accuracy', 0)
        prefetch_effectiveness = ml_stats.get('prefetch_effectiveness', 0)
        
        self.accuracy_label.setText(
            f"Prediction Accuracy: {accuracy:.1f}%\n"
            f"Patterns Learned: {ml_stats.get('patterns_learned', 0)}"
        )
        
        self.prefetch_label.setText(
            f"Prefetch Effectiveness: {prefetch_effectiveness:.1f}%\n"
            f"Successful Prefetches: {ml_stats.get('prefetch_hits', 0)}"
        )
        
        headers = ['Metric', 'Base Algorithm', 'ML-Enhanced', 'Improvement']
        self.table.setRowCount(4)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(headers)
        
        base_faults = base_results['page_faults']
        ml_faults = ml_results['page_faults']
        fault_reduction = ((base_faults - ml_faults) / base_faults * 100) if base_faults > 0 else 0
        
        base_time = base_results.get('average_access_time', 0)
        ml_time = ml_results.get('average_access_time', 0)
        time_reduction = ((base_time - ml_time) / base_time * 100) if base_time > 0 else 0
        
        base_hit_ratio = base_results['hit_ratio'] * 100
        ml_hit_ratio = ml_results['hit_ratio'] * 100
        hit_improvement = ml_hit_ratio - base_hit_ratio
        
        data = [
            ('Page Faults', str(base_faults), str(ml_faults), f"{fault_reduction:.1f}% reduction"),
            ('Hit Ratio', f"{base_hit_ratio:.1f}%", f"{ml_hit_ratio:.1f}%", f"+{hit_improvement:.1f}%"),
            ('Avg Access Time', f"{base_time/1000:.2f} µs", f"{ml_time/1000:.2f} µs", f"{time_reduction:.1f}% faster"),
            ('ML Accuracy', 'N/A', f"{accuracy:.1f}%", f"{ml_stats.get('correct_predictions', 0)}/{ml_stats.get('total_predictions', 0)} correct")
        ]
        
        for i, (metric, base, ml, improvement) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(metric))
            self.table.setItem(i, 1, QTableWidgetItem(base))
            
            ml_item = QTableWidgetItem(ml)
            ml_item.setBackground(QColor(144, 238, 144))
            self.table.setItem(i, 2, ml_item)
            
            imp_item = QTableWidgetItem(improvement)
            imp_item.setForeground(QColor(0, 128, 0))
            imp_item.setBackground(QColor(240, 255, 240))
            self.table.setItem(i, 3, imp_item)
        
        self.table.resizeColumnsToContents()
        
        self.display_charts(base_results, ml_results, ml_stats)
    
    def display_charts(self, base_results, ml_results, ml_stats):
        """Display comparison charts"""
        self.accuracy_canvas.figure.clear()
        ax1 = self.accuracy_canvas.figure.add_subplot(111)
        
        categories = ['Predictions', 'Correct', 'Incorrect']
        total = ml_stats.get('total_predictions', 0)
        correct = ml_stats.get('correct_predictions', 0)
        incorrect = total - correct
        
        values = [total, correct, incorrect]
        colors = ['#2196f3', '#4caf50', '#f44336']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.7)
        ax1.set_ylabel('Count')
        ax1.set_title('ML Prediction Performance')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val}', ha='center', va='bottom')
        
        self.accuracy_canvas.draw()
        
        self.benefit_canvas.figure.clear()
        ax2 = self.benefit_canvas.figure.add_subplot(111)
        
        base_faults = base_results['page_faults']
        ml_faults = ml_results['page_faults']
        
        base_hits = base_results['hits']
        ml_hits = ml_results['hits']
        
        x = [0, 1]
        width = 0.35
        
        ax2.bar([i - width/2 for i in x], [base_faults, ml_faults], 
               width, label='Page Faults', color='#ff6b6b')
        ax2.bar([i + width/2 for i in x], [base_hits, ml_hits], 
               width, label='Hits', color='#51cf66')
        
        ax2.set_ylabel('Count')
        ax2.set_title('Base vs ML-Enhanced Performance')
        ax2.set_xticks(x)
        ax2.set_xticklabels(['Base', 'ML-Enhanced'])
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        self.benefit_canvas.draw()
