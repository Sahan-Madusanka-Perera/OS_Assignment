from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulator.benchmarks import WorkloadBenchmarks
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, LFUAlgorithm, OptimalAlgorithm, ClockAlgorithm
from simulator.simulator import VMSimulator
from simulator.ml_predictor import PredictiveAlgorithm

class BenchmarkWidget(QWidget):
    """Performance benchmarking with standard workloads"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Benchmark Suite - Standard Workloads")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("Test algorithms against industry-standard memory access patterns")
        desc.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(desc)
        
        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Algorithm:"))
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["LRU", "FIFO", "LFU", "Clock", "Optimal"])
        controls_layout.addWidget(self.algo_combo)
        
        controls_layout.addWidget(QLabel("Frames:"))
        self.frames_spinbox = QSpinBox()
        self.frames_spinbox.setRange(2, 10)
        self.frames_spinbox.setValue(4)
        controls_layout.addWidget(self.frames_spinbox)
        
        self.run_button = QPushButton("Run Benchmarks")
        self.run_button.clicked.connect(self.run_benchmarks)
        self.run_button.setStyleSheet("font-weight: bold; padding: 8px;")
        controls_layout.addWidget(self.run_button)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        self.results_table = QTableWidget()
        layout.addWidget(self.results_table)
        
        charts_layout = QHBoxLayout()
        
        self.performance_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        charts_layout.addWidget(self.performance_canvas)
        
        self.ml_impact_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        charts_layout.addWidget(self.ml_impact_canvas)
        
        layout.addLayout(charts_layout)
        
    def run_benchmarks(self):
        """Execute all benchmarks and display results"""
        algo_name = self.algo_combo.currentText()
        num_frames = self.frames_spinbox.value()
        
        benchmarks = WorkloadBenchmarks.get_all_benchmarks()
        
        headers = ['Workload', 'Category', 'Pages', 'Base Faults', 'ML Faults', 
                   'Improvement', 'ML Accuracy']
        self.results_table.setRowCount(len(benchmarks))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        
        results_data = []
        
        for i, (name, bench_data) in enumerate(benchmarks.items()):
            workload = bench_data['workload']
            category = bench_data['category']
            stats = WorkloadBenchmarks.get_workload_stats(workload)
            
            base_result = self.run_algorithm(algo_name, workload, num_frames, use_ml=False)
            ml_result = self.run_algorithm(algo_name, workload, num_frames, use_ml=True)
            
            base_faults = base_result['page_faults']
            ml_faults = ml_result['page_faults']
            improvement = ((base_faults - ml_faults) / base_faults * 100) if base_faults > 0 else 0
            ml_accuracy = ml_result.get('ml_prediction_stats', {}).get('accuracy', 0)
            
            results_data.append({
                'name': name,
                'category': category,
                'pages': stats['unique_pages'],
                'base_faults': base_faults,
                'ml_faults': ml_faults,
                'improvement': improvement,
                'ml_accuracy': ml_accuracy
            })
            
            self.results_table.setItem(i, 0, QTableWidgetItem(name))
            self.results_table.setItem(i, 1, QTableWidgetItem(category))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(stats['unique_pages'])))
            self.results_table.setItem(i, 3, QTableWidgetItem(str(base_faults)))
            self.results_table.setItem(i, 4, QTableWidgetItem(str(ml_faults)))
            
            imp_item = QTableWidgetItem(f"{improvement:.1f}%")
            if improvement > 10:
                imp_item.setBackground(QColor(144, 238, 144))
            elif improvement > 0:
                imp_item.setBackground(QColor(255, 255, 153))
            else:
                imp_item.setBackground(QColor(255, 200, 124))
            self.results_table.setItem(i, 5, imp_item)
            
            self.results_table.setItem(i, 6, QTableWidgetItem(f"{ml_accuracy:.1f}%"))
        
        self.results_table.resizeColumnsToContents()
        self.display_charts(results_data, algo_name)
        
    def run_algorithm(self, algo_name, workload, num_frames, use_ml=False):
        """Execute algorithm on workload"""
        algo_map = {
            'FIFO': FIFOAlgorithm,
            'LRU': LRUAlgorithm,
            'LFU': LFUAlgorithm,
            'Optimal': OptimalAlgorithm,
            'Clock': ClockAlgorithm
        }
        
        base_algo = algo_map[algo_name](num_frames)
        
        if algo_name == 'Optimal':
            base_algo.set_reference_string(workload)
        
        if use_ml:
            algorithm = PredictiveAlgorithm(base_algo)
            if algo_name == 'Optimal':
                algorithm.base_algorithm.set_reference_string(workload)
        else:
            algorithm = base_algo
        
        simulator = VMSimulator(workload, num_frames, algorithm, use_tlb=False)
        results = simulator.run()
        
        if use_ml:
            results['ml_prediction_stats'] = algorithm.get_prediction_stats()
        
        return results
        
    def display_charts(self, results_data, algo_name):
        """Display benchmark results charts"""
        self.performance_canvas.figure.clear()
        ax1 = self.performance_canvas.figure.add_subplot(111)
        
        names = [r['name'] for r in results_data]
        base_faults = [r['base_faults'] for r in results_data]
        ml_faults = [r['ml_faults'] for r in results_data]
        
        x = range(len(names))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], base_faults, width, 
               label='Base', color='#ff6b6b', alpha=0.8)
        ax1.bar([i + width/2 for i in x], ml_faults, width, 
               label='ML-Enhanced', color='#51cf66', alpha=0.8)
        
        ax1.set_xlabel('Workload')
        ax1.set_ylabel('Page Faults')
        ax1.set_title(f'{algo_name} Performance Across Workloads')
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        self.performance_canvas.figure.tight_layout()
        self.performance_canvas.draw()
        
        self.ml_impact_canvas.figure.clear()
        ax2 = self.ml_impact_canvas.figure.add_subplot(111)
        
        improvements = [r['improvement'] for r in results_data]
        colors = ['#4caf50' if imp > 10 else '#ffc107' if imp > 0 else '#ff9800' 
                  for imp in improvements]
        
        bars = ax2.bar(names, improvements, color=colors, alpha=0.8)
        ax2.set_ylabel('Improvement (%)')
        ax2.set_title('ML Prediction Impact')
        ax2.set_xticklabels(names, rotation=45, ha='right')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, imp in zip(bars, improvements):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{imp:.1f}%', ha='center', va='bottom' if imp > 0 else 'top',
                    fontsize=8)
        
        self.ml_impact_canvas.figure.tight_layout()
        self.ml_impact_canvas.draw()
