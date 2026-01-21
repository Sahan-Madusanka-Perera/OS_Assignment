"""
Modern Comparison Widget with beautiful charts and animations
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QFrame, QHeaderView,
                             QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE, CHART_COLORS
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm, ClockAlgorithm, LFUAlgorithm
from simulator.simulator import VMSimulator
from utils.statistics import Statistics


class ComparisonWidget(QWidget):
    """Widget to compare all algorithms side-by-side"""
    
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
                    stop:0 rgba(14, 165, 168, 0.2), stop:1 rgba(56, 189, 248, 0.2));
                border-radius: 12px;
                padding: 8px;
            }}
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("⚖️ Algorithm Comparison")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        
        layout.addWidget(title_frame)
        
        # Recommendation panel
        self.recommendation_frame = QFrame()
        self.recommendation_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(16, 185, 129, 0.15);
                border: 2px solid {COLORS['success']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        rec_layout = QHBoxLayout(self.recommendation_frame)
        
        rec_icon = QLabel("🏆")
        rec_icon.setStyleSheet("font-size: 28px;")
        rec_layout.addWidget(rec_icon)
        
        self.recommendation_label = QLabel("Run comparison to see recommendation")
        self.recommendation_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 600;
        """)
        self.recommendation_label.setWordWrap(True)
        rec_layout.addWidget(self.recommendation_label, 1)
        
        layout.addWidget(self.recommendation_frame)
        
        # Results table
        table_label = QLabel("📊 Detailed Comparison")
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
            QTableWidget::item:selected {{
                background-color: rgba(14, 165, 168, 0.3);
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['bg_light']}, stop:1 {COLORS['bg_medium']});
                color: {COLORS['text_primary']};
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid {COLORS['success']};
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
        charts_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setContentsMargins(8, 8, 8, 8)
        
        self.faults_canvas = FigureCanvas(Figure(figsize=(7, 5), facecolor=COLORS['bg_medium']))
        charts_layout.addWidget(self.faults_canvas)
        
        self.performance_canvas = FigureCanvas(Figure(figsize=(7, 5), facecolor=COLORS['bg_medium']))
        charts_layout.addWidget(self.performance_canvas)
        
        layout.addWidget(charts_frame)
    
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
        self.recommendation_label.setText(f"<b>Recommended:</b> {recommendation}")
        
        self.display_results_table(results, rankings)
        self.display_charts(results)
        return results
    
    def display_results_table(self, results, rankings):
        """Display comparison table"""
        headers = ['🏅', 'Algorithm', '⭐ Score', '❌ Faults', '✅ Hits', '📊 Hit %', '💀 Fault %']
        if results and 'tlb_stats' in results[0][1]:
            headers.extend(['⚡ TLB Hits', '⚡ TLB %'])
        headers.append('⏱️ Avg (µs)')
        
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        
        rank_map = {r['algorithm']: r for r in rankings}
        
        for i, (name, result) in enumerate(results):
            rank_info = rank_map.get(name, {})
            col = 0
            
            # Rank with medal
            rank = rank_info.get('rank', '-')
            rank_icons = {1: '🥇', 2: '🥈', 3: '🥉'}
            rank_text = rank_icons.get(rank, str(rank))
            rank_item = QTableWidgetItem(rank_text)
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            rank_item.setFont(QFont("Helvetica Neue", 14))
            self.results_table.setItem(i, col, rank_item)
            col += 1
            
            # Algorithm name
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
            name_item.setForeground(QBrush(QColor(COLORS['primary_light'])))
            self.results_table.setItem(i, col, name_item)
            col += 1
            
            # Efficiency score with color coding
            efficiency = rank_info.get('efficiency_score', 0)
            eff_item = QTableWidgetItem(f"{efficiency:.1f}")
            eff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            eff_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
            
            if efficiency >= 80:
                eff_item.setForeground(QBrush(QColor(COLORS['success_light'])))
            elif efficiency >= 60:
                eff_item.setForeground(QBrush(QColor(COLORS['warning_light'])))
            else:
                eff_item.setForeground(QBrush(QColor(COLORS['error_light'])))
            self.results_table.setItem(i, col, eff_item)
            col += 1
            
            # Page faults
            faults_item = QTableWidgetItem(str(result['page_faults']))
            faults_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            faults_item.setForeground(QBrush(QColor(COLORS['error_light'])))
            self.results_table.setItem(i, col, faults_item)
            col += 1
            
            # Hits
            hits_item = QTableWidgetItem(str(result['hits']))
            hits_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            hits_item.setForeground(QBrush(QColor(COLORS['success_light'])))
            self.results_table.setItem(i, col, hits_item)
            col += 1
            
            # Hit ratio
            hit_item = QTableWidgetItem(f"{result['hit_ratio']:.1%}")
            hit_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(i, col, hit_item)
            col += 1
            
            # Fault ratio
            fault_item = QTableWidgetItem(f"{result['fault_ratio']:.1%}")
            fault_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(i, col, fault_item)
            col += 1
            
            # TLB stats
            if 'tlb_stats' in result:
                tlb = result['tlb_stats']
                tlb_hits_item = QTableWidgetItem(str(tlb['hits']))
                tlb_hits_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tlb_hits_item.setForeground(QBrush(QColor(COLORS['accent'])))
                self.results_table.setItem(i, col, tlb_hits_item)
                col += 1
                
                tlb_ratio_item = QTableWidgetItem(f"{tlb['hit_ratio']:.1%}")
                tlb_ratio_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.results_table.setItem(i, col, tlb_ratio_item)
                col += 1
            
            # Average access time
            if 'average_access_time' in result:
                avg_time_us = result['average_access_time'] / 1000
                time_item = QTableWidgetItem(f"{avg_time_us:.2f}")
                time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.results_table.setItem(i, col, time_item)
        
        # Resize columns
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Highlight best row
        best_idx = min(range(len(results)), key=lambda i: results[i][1]['page_faults'])
        for col in range(self.results_table.columnCount()):
            item = self.results_table.item(best_idx, col)
            if item:
                item.setBackground(QBrush(QColor(16, 185, 129, 40)))
    
    def display_charts(self, results):
        """Display comparison charts with modern styling"""
        # Faults vs Hits chart
        self.faults_canvas.figure.clear()
        self.faults_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax1 = self.faults_canvas.figure.add_subplot(111)
        ax1.set_facecolor(COLORS['bg_light'])
        
        names = [r[0] for r in results]
        faults = [r[1]['page_faults'] for r in results]
        hits = [r[1]['hits'] for r in results]
        
        x = np.arange(len(names))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, faults, width, label='Page Faults', 
                       color=COLORS['error'], alpha=0.85, edgecolor='white', linewidth=0.5)
        bars2 = ax1.bar(x + width/2, hits, width, label='Hits', 
                       color=COLORS['success'], alpha=0.85, edgecolor='white', linewidth=0.5)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=COLORS['text_primary'])
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=COLORS['text_primary'])
        
        ax1.set_xlabel('Algorithm', color=COLORS['text_primary'], fontweight='500')
        ax1.set_ylabel('Count', color=COLORS['text_primary'], fontweight='500')
        ax1.set_title('Page Faults vs Hits', color=COLORS['text_primary'], 
                     fontsize=13, fontweight='600', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, color=COLORS['text_secondary'])
        ax1.tick_params(colors=COLORS['text_secondary'])
        ax1.legend(facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                  labelcolor=COLORS['text_primary'])
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_color(COLORS['border'])
        ax1.spines['left'].set_color(COLORS['border'])
        ax1.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.faults_canvas.figure.tight_layout()
        self.faults_canvas.draw()
        
        # Performance chart
        self.performance_canvas.figure.clear()
        self.performance_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax2 = self.performance_canvas.figure.add_subplot(111)
        ax2.set_facecolor(COLORS['bg_light'])
        
        if results and 'average_access_time' in results[0][1]:
            access_times = [r[1]['average_access_time'] / 1000 for r in results]
            colors = CHART_COLORS[:len(names)]
            
            bars = ax2.bar(names, access_times, color=colors, alpha=0.85,
                          edgecolor='white', linewidth=0.5)
            ax2.set_ylabel('Average Access Time (µs)', color=COLORS['text_primary'], fontweight='500')
            ax2.set_title('Memory Access Performance', color=COLORS['text_primary'],
                         fontsize=13, fontweight='600', pad=15)
            
            for bar, time_us in zip(bars, access_times):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{time_us:.1f}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color=COLORS['text_primary'])
        else:
            hit_ratios = [r[1]['hit_ratio'] * 100 for r in results]
            colors = CHART_COLORS[:len(names)]
            
            bars = ax2.bar(names, hit_ratios, color=colors, alpha=0.85,
                          edgecolor='white', linewidth=0.5)
            ax2.set_ylabel('Hit Ratio (%)', color=COLORS['text_primary'], fontweight='500')
            ax2.set_title('Algorithm Efficiency', color=COLORS['text_primary'],
                         fontsize=13, fontweight='600', pad=15)
            ax2.set_ylim(0, 100)
            
            for bar, ratio in zip(bars, hit_ratios):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{ratio:.0f}%', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color=COLORS['text_primary'])
        
        ax2.tick_params(colors=COLORS['text_secondary'])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_color(COLORS['border'])
        ax2.spines['left'].set_color(COLORS['border'])
        ax2.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.performance_canvas.figure.tight_layout()
        self.performance_canvas.draw()
