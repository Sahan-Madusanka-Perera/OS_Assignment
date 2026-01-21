"""
Modern ML Prediction Widget
Beautiful visualization of ML-enhanced page replacement
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QFrame, QHeaderView,
                             QAbstractItemView, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE, CHART_COLORS


class MLPredictionWidget(QWidget):
    """Widget to visualize ML prediction performance"""
    
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
        
        title = QLabel("🤖 Machine Learning Prediction Analysis")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        
        desc = QLabel("Uses pattern recognition to predict and prefetch pages before they're needed")
        desc.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_muted']};
            font-style: italic;
        """)
        title_layout.addWidget(desc)
        
        layout.addWidget(title_frame)
        
        # Stats Cards Row
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(16)
        
        self.accuracy_card = self.create_stat_card("🎯", "Prediction Accuracy", "0%", "secondary")
        stats_layout.addWidget(self.accuracy_card)
        
        self.prefetch_card = self.create_stat_card("⚡", "Prefetch Effectiveness", "0%", "accent")
        stats_layout.addWidget(self.prefetch_card)
        
        self.patterns_card = self.create_stat_card("🧠", "Patterns Learned", "0", "primary")
        stats_layout.addWidget(self.patterns_card)
        
        self.improvement_card = self.create_stat_card("📈", "Improvement", "0%", "success")
        stats_layout.addWidget(self.improvement_card)
        
        layout.addWidget(stats_frame)
        
        # Comparison table
        table_label = QLabel("📊 Base vs ML-Enhanced Comparison")
        table_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding: 8px 0;
        """)
        layout.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_medium']};
                alternate-background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['bg_light']}, stop:1 {COLORS['bg_medium']});
                color: {COLORS['text_primary']};
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid {COLORS['secondary']};
                font-weight: 600;
            }}
        """)
        layout.addWidget(self.table)
        
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
        
        self.accuracy_canvas = FigureCanvas(Figure(figsize=(6, 5), facecolor=COLORS['bg_medium']))
        self.accuracy_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        charts_layout.addWidget(self.accuracy_canvas)
        
        self.benefit_canvas = FigureCanvas(Figure(figsize=(6, 5), facecolor=COLORS['bg_medium']))
        self.benefit_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        charts_layout.addWidget(self.benefit_canvas)
        
        layout.addWidget(charts_frame)
        
    def create_stat_card(self, icon, title, value, color_type):
        """Create a modern stat card"""
        card = QFrame()
        
        color_map = {
            'primary': (COLORS['primary'], COLORS['primary_dark']),
            'secondary': (COLORS['secondary'], '#d97706'),
            'success': (COLORS['success'], '#16a34a'),
            'accent': (COLORS['accent'], '#0284c7'),
        }
        
        c1, c2 = color_map.get(color_type, (COLORS['primary'], COLORS['primary_dark']))
        
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c1}, stop:1 {c2});
                border: none;
                border-radius: 12px;
                min-width: 160px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        header.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            font-size: 10px;
            font-weight: 500;
        """)
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: 700;
        """)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def display_ml_comparison(self, base_results, ml_results):
        """Display comparison between base and ML-enhanced algorithms"""
        ml_stats = ml_results.get('ml_prediction_stats', {})
        
        accuracy = ml_stats.get('accuracy', 0)
        prefetch_effectiveness = ml_stats.get('prefetch_effectiveness', 0)
        patterns = ml_stats.get('patterns_learned', 0)
        
        # Calculate improvement
        base_faults = base_results['page_faults']
        ml_faults = ml_results['page_faults']
        improvement = ((base_faults - ml_faults) / base_faults * 100) if base_faults > 0 else 0
        
        # Update stat cards
        self.accuracy_card.value_label.setText(f"{accuracy:.1f}%")
        self.prefetch_card.value_label.setText(f"{prefetch_effectiveness:.1f}%")
        self.patterns_card.value_label.setText(str(patterns))
        self.improvement_card.value_label.setText(f"+{improvement:.1f}%")
        
        # Update table
        headers = ['📋 Metric', '📊 Base Algorithm', '🤖 ML-Enhanced', '📈 Improvement']
        self.table.setRowCount(4)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(headers)
        
        base_time = base_results.get('average_access_time', 0)
        ml_time = ml_results.get('average_access_time', 0)
        time_reduction = ((base_time - ml_time) / base_time * 100) if base_time > 0 else 0
        
        base_hit_ratio = base_results['hit_ratio'] * 100
        ml_hit_ratio = ml_results['hit_ratio'] * 100
        hit_improvement = ml_hit_ratio - base_hit_ratio
        
        data = [
            ('Page Faults', str(base_faults), str(ml_faults), f"{improvement:+.1f}% reduction"),
            ('Hit Ratio', f"{base_hit_ratio:.1f}%", f"{ml_hit_ratio:.1f}%", f"{hit_improvement:+.1f}%"),
            ('Avg Access Time', f"{base_time/1000:.2f} µs", f"{ml_time/1000:.2f} µs", f"{time_reduction:+.1f}% faster"),
            ('ML Accuracy', 'N/A', f"{accuracy:.1f}%", f"{ml_stats.get('correct_predictions', 0)}/{ml_stats.get('total_predictions', 0)} correct")
        ]
        
        for i, (metric, base, ml, imp) in enumerate(data):
            # Metric name
            metric_item = QTableWidgetItem(metric)
            metric_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
            self.table.setItem(i, 0, metric_item)
            
            # Base value
            base_item = QTableWidgetItem(base)
            base_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            base_item.setForeground(QBrush(QColor(COLORS['text_secondary'])))
            self.table.setItem(i, 1, base_item)
            
            # ML value (highlighted)
            ml_item = QTableWidgetItem(ml)
            ml_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ml_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
            ml_item.setForeground(QBrush(QColor(COLORS['secondary'])))
            self.table.setItem(i, 2, ml_item)
            
            # Improvement (colored based on value)
            imp_item = QTableWidgetItem(imp)
            imp_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            imp_item.setFont(QFont("Helvetica Neue", 10, QFont.Weight.Bold))
            imp_item.setForeground(QBrush(QColor(COLORS['success_light'])))
            self.table.setItem(i, 3, imp_item)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.display_charts(base_results, ml_results, ml_stats)
    
    def display_charts(self, base_results, ml_results, ml_stats):
        """Display comparison charts"""
        # Accuracy chart
        self.accuracy_canvas.figure.clear()
        self.accuracy_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax1 = self.accuracy_canvas.figure.add_subplot(111)
        ax1.set_facecolor(COLORS['bg_light'])
        
        total = ml_stats.get('total_predictions', 0)
        correct = ml_stats.get('correct_predictions', 0)
        incorrect = total - correct
        
        if total > 0:
            # Donut chart
            sizes = [correct, incorrect]
            colors = [COLORS['success'], COLORS['error']]
            
            wedges, texts = ax1.pie(sizes, colors=colors, startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor=COLORS['bg_medium'],
                                                   linewidth=2))
            
            accuracy = ml_stats.get('accuracy', 0)
            ax1.text(0, 0.05, f'{accuracy:.0f}%', ha='center', va='center',
                    fontsize=24, fontweight='bold', color=COLORS['text_primary'])
            ax1.text(0, -0.15, 'Accuracy', ha='center', va='center',
                    fontsize=10, color=COLORS['text_muted'])
            
            ax1.legend(['Correct', 'Incorrect'], loc='lower center', 
                      bbox_to_anchor=(0.5, -0.1),
                      facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                      labelcolor=COLORS['text_primary'], fontsize=9)
        
        ax1.set_title('ML Prediction Accuracy', color=COLORS['text_primary'],
                     fontsize=13, fontweight='600', pad=20)
        
        self.accuracy_canvas.figure.tight_layout()
        self.accuracy_canvas.draw()
        
        # Benefit chart
        self.benefit_canvas.figure.clear()
        self.benefit_canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax2 = self.benefit_canvas.figure.add_subplot(111)
        ax2.set_facecolor(COLORS['bg_light'])
        
        categories = ['Page Faults', 'Hits']
        base_vals = [base_results['page_faults'], base_results['hits']]
        ml_vals = [ml_results['page_faults'], ml_results['hits']]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, base_vals, width, label='Base', 
                       color=COLORS['text_muted'], alpha=0.7,
                       edgecolor='white', linewidth=0.5)
        bars2 = ax2.bar(x + width/2, ml_vals, width, label='ML-Enhanced', 
                       color=COLORS['secondary'], alpha=0.85,
                       edgecolor='white', linewidth=0.5)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom',
                    fontsize=9, color=COLORS['text_primary'])
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=COLORS['text_primary'])
        
        ax2.set_ylabel('Count', color=COLORS['text_primary'], fontweight='500')
        ax2.set_title('Performance Comparison', color=COLORS['text_primary'],
                     fontsize=13, fontweight='600', pad=15)
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories, color=COLORS['text_secondary'])
        ax2.tick_params(colors=COLORS['text_secondary'])
        ax2.legend(facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                  labelcolor=COLORS['text_primary'], fontsize=9)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_color(COLORS['border'])
        ax2.spines['left'].set_color(COLORS['border'])
        ax2.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.benefit_canvas.figure.tight_layout()
        self.benefit_canvas.draw()
