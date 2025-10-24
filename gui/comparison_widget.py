from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm, ClockAlgorithm
from simulator.simulator import VMSimulator

class ComparisonWidget(QWidget):
    """Widget to compare all algorithms side-by-side"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Algorithm Comparison")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        self.results_table = QTableWidget()
        layout.addWidget(self.results_table)
        
        charts_layout = QHBoxLayout()
        
        self.faults_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        charts_layout.addWidget(self.faults_canvas)
        
        self.performance_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        charts_layout.addWidget(self.performance_canvas)
        
        layout.addLayout(charts_layout)
    
    def compare_algorithms(self, reference_string, num_frames, use_tlb=True):
        """Run all algorithms and display comparison"""
        algorithms = [
            ('FIFO', FIFOAlgorithm),
            ('LRU', LRUAlgorithm),
            ('Optimal', OptimalAlgorithm),
            ('Clock', ClockAlgorithm)
        ]
        
        results = []
        for name, algo_class in algorithms:
            algo = algo_class(num_frames)
            if name == 'Optimal':
                algo.set_reference_string(reference_string)
            
            simulator = VMSimulator(reference_string, num_frames, algo, use_tlb=use_tlb)
            result = simulator.run()
            results.append((name, result))
        
        self.display_results_table(results)
        self.display_charts(results)
    
    def display_results_table(self, results):
        """Display comparison table"""
        headers = ['Algorithm', 'Page Faults', 'Hits', 'Hit Ratio', 'Fault Ratio']
        if results and 'tlb_stats' in results[0][1]:
            headers.extend(['TLB Hits', 'TLB Hit Ratio'])
        
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        
        for i, (name, result) in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(name))
            self.results_table.setItem(i, 1, QTableWidgetItem(str(result['page_faults'])))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(result['hits'])))
            self.results_table.setItem(i, 3, QTableWidgetItem(f"{result['hit_ratio']:.2%}"))
            self.results_table.setItem(i, 4, QTableWidgetItem(f"{result['fault_ratio']:.2%}"))
            
            if 'tlb_stats' in result:
                tlb = result['tlb_stats']
                self.results_table.setItem(i, 5, QTableWidgetItem(str(tlb['hits'])))
                self.results_table.setItem(i, 6, QTableWidgetItem(f"{tlb['hit_ratio']:.2%}"))
        
        self.results_table.resizeColumnsToContents()
        
        best_idx = min(range(len(results)), key=lambda i: results[i][1]['page_faults'])
        for col in range(self.results_table.columnCount()):
            item = self.results_table.item(best_idx, col)
            if item:
                item.setBackground(Qt.GlobalColor.lightGray)
    
    def display_charts(self, results):
        """Display comparison charts"""
        self.faults_canvas.figure.clear()
        ax1 = self.faults_canvas.figure.add_subplot(111)
        
        names = [r[0] for r in results]
        faults = [r[1]['page_faults'] for r in results]
        hits = [r[1]['hits'] for r in results]
        
        x = range(len(names))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], faults, width, label='Page Faults', color='#ff6b6b')
        ax1.bar([i + width/2 for i in x], hits, width, label='Hits', color='#51cf66')
        
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Count')
        ax1.set_title('Page Faults vs Hits')
        ax1.set_xticks(x)
        ax1.set_xticklabels(names)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        self.faults_canvas.draw()
        
        self.performance_canvas.figure.clear()
        ax2 = self.performance_canvas.figure.add_subplot(111)
        
        hit_ratios = [r[1]['hit_ratio'] * 100 for r in results]
        colors = ['#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
        
        bars = ax2.bar(names, hit_ratios, color=colors)
        ax2.set_ylabel('Hit Ratio (%)')
        ax2.set_title('Algorithm Performance')
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, ratio in zip(bars, hit_ratios):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{ratio:.1f}%', ha='center', va='bottom')
        
        self.performance_canvas.draw()
