"""
Modern Benchmark Widget
Performance testing with beautiful visualizations
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, 
                             QComboBox, QSpinBox, QFrame, QHeaderView,
                             QAbstractItemView, QProgressBar, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE, CHART_COLORS
from simulator.benchmarks import WorkloadBenchmarks
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, LFUAlgorithm, OptimalAlgorithm, ClockAlgorithm
from simulator.simulator import VMSimulator
from simulator.ml_predictor import PredictiveAlgorithm


class BenchmarkWidget(QWidget):
    """Performance benchmarking with standard workloads"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        plt.rcParams.update(MATPLOTLIB_STYLE)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)
        
        # Title
        title_frame = QFrame()
        title_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(14, 165, 168, 0.2), stop:1 rgba(245, 158, 11, 0.2));
                border-radius: 12px;
                padding: 8px;
            }}
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("📊 Benchmark Suite")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Test algorithms against industry-standard memory access patterns")
        desc.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_muted']};
        """)
        title_layout.addWidget(desc)
        
        layout.addWidget(title_frame)
        
        # Controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(20)
        
        # Algorithm selector
        algo_container = QVBoxLayout()
        algo_label = QLabel("🔄 Algorithm")
        algo_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600;")
        algo_container.addWidget(algo_label)
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["LRU", "FIFO", "LFU", "Clock", "Optimal"])
        self.algo_combo.setMinimumWidth(120)
        algo_container.addWidget(self.algo_combo)
        controls_layout.addLayout(algo_container)
        
        # Frames selector
        frames_container = QVBoxLayout()
        frames_label = QLabel("🔲 Frames")
        frames_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600;")
        frames_container.addWidget(frames_label)
        
        self.frames_spinbox = QSpinBox()
        self.frames_spinbox.setRange(2, 10)
        self.frames_spinbox.setValue(4)
        self.frames_spinbox.setMinimumWidth(80)
        frames_container.addWidget(self.frames_spinbox)
        controls_layout.addLayout(frames_container)
        
        controls_layout.addStretch()
        
        # Run button
        self.run_button = QPushButton("🚀 Run Benchmarks")
        self.run_button.clicked.connect(self.run_benchmarks)
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_button.setMinimumHeight(50)
        self.run_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['warning']}, stop:1 #ea580c);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 32px;
                font-weight: 700;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['warning_light']}, stop:1 {COLORS['warning']});
            }}
        """)
        controls_layout.addWidget(self.run_button)
        
        layout.addWidget(controls_frame)
        
        # Results table
        table_label = QLabel("📋 Benchmark Results")
        table_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding: 8px 0;
        """)
        layout.addWidget(table_label)
        
        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setShowGrid(False)
        self.results_table.setFixedHeight(260)
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_medium']};
                alternate-background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QTableWidget::item {{
                padding: 10px 12px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['bg_light']}, stop:1 {COLORS['bg_medium']});
                color: {COLORS['text_primary']};
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid {COLORS['warning']};
                font-weight: 600;
            }}
        """)
        layout.addWidget(self.results_table)
        
        # Charts
        charts_label = QLabel("📈 Visual Analysis")
        charts_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding: 8px 0;
        """)
        layout.addWidget(charts_label)
        
        charts_frame = QFrame()
        fixed_chart_height = 340
        charts_frame.setFixedHeight(fixed_chart_height)
        charts_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setContentsMargins(8, 8, 8, 8)
        
        self.performance_canvas = FigureCanvas(Figure(figsize=(7, 5), facecolor=COLORS['bg_medium']))
        self.performance_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        charts_layout.addWidget(self.performance_canvas)
        
        self.ml_impact_canvas = FigureCanvas(Figure(figsize=(7, 5), facecolor=COLORS['bg_medium']))
        self.ml_impact_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        charts_layout.addWidget(self.ml_impact_canvas)
        
        layout.addWidget(charts_frame)
        
    def run_benchmarks(self):
        """Execute all benchmarks and display results"""
        algo_name = self.algo_combo.currentText()
        num_frames = self.frames_spinbox.value()
        
        self.run_button.setText("⏳ Running...")
        self.run_button.setEnabled(False)
        
        # Use QTimer to allow UI to update
        QTimer.singleShot(100, lambda: self._execute_benchmarks(algo_name, num_frames))
        
    def _execute_benchmarks(self, algo_name, num_frames):
        """Execute benchmarks in separate call for UI responsiveness"""
        try:
            benchmarks = WorkloadBenchmarks.get_all_benchmarks()
            
            headers = ['📋 Workload', '📁 Category', '📄 Pages', '❌ Base', '🤖 ML', 
                       '📈 Improvement', '🎯 Accuracy']
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
                
                # Workload name
                name_item = QTableWidgetItem(name)
                name_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
                name_item.setForeground(QBrush(QColor(COLORS['primary_light'])))
                self.results_table.setItem(i, 0, name_item)
                
                # Category with icon
                cat_icons = {'Locality': '🎯', 'Sequential': '➡️', 'Cyclic': '🔄', 
                            'Random': '🎲', 'Temporal': '⏰', 'Spatial': '📍'}
                cat_icon = cat_icons.get(category, '📋')
                cat_item = QTableWidgetItem(f"{cat_icon} {category}")
                cat_item.setForeground(QBrush(QColor(COLORS['text_secondary'])))
                self.results_table.setItem(i, 1, cat_item)
                
                # Pages
                pages_item = QTableWidgetItem(str(stats['unique_pages']))
                pages_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.results_table.setItem(i, 2, pages_item)
                
                # Base faults
                base_item = QTableWidgetItem(str(base_faults))
                base_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                base_item.setForeground(QBrush(QColor(COLORS['error_light'])))
                self.results_table.setItem(i, 3, base_item)
                
                # ML faults
                ml_item = QTableWidgetItem(str(ml_faults))
                ml_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                ml_item.setForeground(QBrush(QColor(COLORS['success_light'])))
                self.results_table.setItem(i, 4, ml_item)
                
                # Improvement
                imp_item = QTableWidgetItem(f"{improvement:+.1f}%")
                imp_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                imp_item.setFont(QFont("Helvetica Neue", 10, QFont.Weight.Bold))
                if improvement > 10:
                    imp_item.setForeground(QBrush(QColor(COLORS['success_light'])))
                elif improvement > 0:
                    imp_item.setForeground(QBrush(QColor(COLORS['warning_light'])))
                else:
                    imp_item.setForeground(QBrush(QColor(COLORS['text_muted'])))
                self.results_table.setItem(i, 5, imp_item)
                
                # Accuracy
                acc_item = QTableWidgetItem(f"{ml_accuracy:.1f}%")
                acc_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.results_table.setItem(i, 6, acc_item)
            
            header = self.results_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            
            self.display_charts(results_data, algo_name)
            
        finally:
            self.run_button.setText("🚀 Run Benchmarks")
            self.run_button.setEnabled(True)
        
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
        # Performance comparison chart
        self.performance_canvas.figure.clear()
        self.performance_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax1 = self.performance_canvas.figure.add_subplot(111)
        ax1.set_facecolor(COLORS['bg_light'])
        
        names = [r['name'] for r in results_data]
        base_faults = [r['base_faults'] for r in results_data]
        ml_faults = [r['ml_faults'] for r in results_data]
        
        x = np.arange(len(names))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, base_faults, width, label='Base', 
                       color=COLORS['error'], alpha=0.7,
                       edgecolor='white', linewidth=0.5)
        bars2 = ax1.bar(x + width/2, ml_faults, width, label='ML-Enhanced', 
                       color=COLORS['success'], alpha=0.85,
                       edgecolor='white', linewidth=0.5)
        
        ax1.set_xlabel('Workload', color=COLORS['text_primary'], fontweight='500')
        ax1.set_ylabel('Page Faults', color=COLORS['text_primary'], fontweight='500')
        ax1.set_title(f'{algo_name} Performance Across Workloads', 
                     color=COLORS['text_primary'], fontsize=12, fontweight='600', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax1.tick_params(colors=COLORS['text_secondary'])
        ax1.legend(facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                  labelcolor=COLORS['text_primary'], fontsize=9)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_color(COLORS['border'])
        ax1.spines['left'].set_color(COLORS['border'])
        ax1.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.performance_canvas.figure.tight_layout()
        self.performance_canvas.draw()
        
        # ML impact chart
        self.ml_impact_canvas.figure.clear()
        self.ml_impact_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax2 = self.ml_impact_canvas.figure.add_subplot(111)
        ax2.set_facecolor(COLORS['bg_light'])
        
        improvements = [r['improvement'] for r in results_data]
        colors = [COLORS['success'] if imp > 10 else COLORS['warning'] if imp > 0 
                  else COLORS['text_muted'] for imp in improvements]
        
        bars = ax2.bar(names, improvements, color=colors, alpha=0.85,
                      edgecolor='white', linewidth=0.5)
        
        for bar, imp in zip(bars, improvements):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{imp:+.0f}%', ha='center', 
                    va='bottom' if imp >= 0 else 'top',
                    fontsize=8, fontweight='bold', color=COLORS['text_primary'])
        
        ax2.axhline(y=0, color=COLORS['text_muted'], linestyle='-', linewidth=1, alpha=0.5)
        ax2.set_ylabel('Improvement (%)', color=COLORS['text_primary'], fontweight='500')
        ax2.set_title('ML Prediction Impact', color=COLORS['text_primary'],
                     fontsize=12, fontweight='600', pad=15)
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax2.tick_params(colors=COLORS['text_secondary'])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_color(COLORS['border'])
        ax2.spines['left'].set_color(COLORS['border'])
        ax2.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.ml_impact_canvas.figure.tight_layout()
        self.ml_impact_canvas.draw()
