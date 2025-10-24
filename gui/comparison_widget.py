from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm, ClockAlgorithm, LFUAlgorithm
from simulator.simulator import VMSimulator
from utils.statistics import Statistics

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
        
        self.recommendation_label = QLabel()
        self.recommendation_label.setStyleSheet("font-size: 13px; font-weight: bold; padding: 12px; background-color: #d4edda; border: 2px solid #28a745; border-radius: 5px; color: #155724;")
        self.recommendation_label.setWordWrap(True)
        layout.addWidget(self.recommendation_label)
        
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
            ('LFU', LFUAlgorithm),
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
        
        rankings = Statistics.rank_algorithms(results)
        recommendation = Statistics.get_recommendation(rankings)
        self.recommendation_label.setText(f"Recommendation: {recommendation}")
        
        self.display_results_table(results, rankings)
        self.display_charts(results)
        return results
    
    def display_results_table(self, results, rankings):
        """Display comparison table"""
        headers = ['Rank', 'Algorithm', 'Efficiency', 'Page Faults', 'Hits', 'Hit Ratio', 'Fault Ratio']
        if results and 'tlb_stats' in results[0][1]:
            headers.extend(['TLB Hits', 'TLB Hit Ratio'])
        headers.append('Avg Access (µs)')
        
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        
        rank_map = {r['algorithm']: r for r in rankings}
        
        for i, (name, result) in enumerate(results):
            rank_info = rank_map.get(name, {})
            col = 0
            
            rank_item = QTableWidgetItem(str(rank_info.get('rank', '-')))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(i, col, rank_item)
            col += 1
            
            self.results_table.setItem(i, col, QTableWidgetItem(name))
            col += 1
            
            efficiency = rank_info.get('efficiency_score', 0)
            eff_item = QTableWidgetItem(f"{efficiency:.1f}")
            eff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if efficiency >= 80:
                eff_item.setBackground(QColor(144, 238, 144))
                eff_item.setForeground(QColor(0, 0, 0))
            elif efficiency >= 60:
                eff_item.setBackground(QColor(255, 255, 153))
                eff_item.setForeground(QColor(0, 0, 0))
            elif efficiency >= 40:
                eff_item.setBackground(QColor(255, 200, 124))
                eff_item.setForeground(QColor(0, 0, 0))
            else:
                eff_item.setBackground(QColor(255, 182, 193))
                eff_item.setForeground(QColor(0, 0, 0))
            self.results_table.setItem(i, col, eff_item)
            col += 1
            
            self.results_table.setItem(i, col, QTableWidgetItem(str(result['page_faults'])))
            col += 1
            self.results_table.setItem(i, col, QTableWidgetItem(str(result['hits'])))
            col += 1
            self.results_table.setItem(i, col, QTableWidgetItem(f"{result['hit_ratio']:.2%}"))
            col += 1
            self.results_table.setItem(i, col, QTableWidgetItem(f"{result['fault_ratio']:.2%}"))
            col += 1
            
            if 'tlb_stats' in result:
                tlb = result['tlb_stats']
                self.results_table.setItem(i, col, QTableWidgetItem(str(tlb['hits'])))
                col += 1
                self.results_table.setItem(i, col, QTableWidgetItem(f"{tlb['hit_ratio']:.2%}"))
                col += 1
            
            if 'average_access_time' in result:
                avg_time_us = result['average_access_time'] / 1000
                self.results_table.setItem(i, col, QTableWidgetItem(f"{avg_time_us:.2f}"))
        
        self.results_table.resizeColumnsToContents()
        
        best_idx = min(range(len(results)), key=lambda i: results[i][1]['page_faults'])
        for col in range(self.results_table.columnCount()):
            item = self.results_table.item(best_idx, col)
            if item:
                item.setBackground(QColor(220, 220, 220))
                item.setForeground(QColor(0, 0, 0))
    
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
        
        if results and 'average_access_time' in results[0][1]:
            access_times = [r[1]['average_access_time'] / 1000 for r in results]
            colors = ['#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#ff9ff3']
            
            bars = ax2.bar(names, access_times, color=colors)
            ax2.set_ylabel('Average Access Time (µs)')
            ax2.set_title('Memory Access Performance')
            ax2.grid(axis='y', alpha=0.3)
            
            for bar, time_us in zip(bars, access_times):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time_us:.1f}', ha='center', va='bottom', fontsize=8)
        else:
            hit_ratios = [r[1]['hit_ratio'] * 100 for r in results]
            colors = ['#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#ff9ff3']
            
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
