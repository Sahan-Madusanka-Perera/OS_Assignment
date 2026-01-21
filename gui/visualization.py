"""
Modern Visualization Widget for Virtual Memory Simulator
Beautiful charts and animated data displays
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QFrame, QHeaderView,
                             QAbstractItemView, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QColor, QBrush, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE, CHART_COLORS, CARD_STYLE


class VisualizationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_matplotlib_style()

    def apply_matplotlib_style(self):
        """Apply dark theme to matplotlib"""
        plt.rcParams.update(MATPLOTLIB_STYLE)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)
        
        # Stats Cards Row
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(16)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        self.algo_card = self.create_stat_card("🔄", "Algorithm", "--", "primary")
        stats_layout.addWidget(self.algo_card)
        
        self.faults_card = self.create_stat_card("❌", "Page Faults", "0", "error")
        stats_layout.addWidget(self.faults_card)
        
        self.hits_card = self.create_stat_card("✅", "Hits", "0", "success")
        stats_layout.addWidget(self.hits_card)
        
        self.ratio_card = self.create_stat_card("📊", "Hit Ratio", "0%", "accent")
        stats_layout.addWidget(self.ratio_card)
        
        layout.addWidget(stats_frame)

        # Step-by-step Table with modern styling
        table_label = QLabel("📋 Step-by-Step Execution")
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
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(200)
        self.table.setMaximumHeight(350)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_medium']};
                alternate-background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                gridline-color: transparent;
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
                border-bottom: 2px solid {COLORS['primary']};
                font-weight: 600;
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.table)

        # Charts Section
        charts_label = QLabel("📈 Performance Analysis")
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
                padding: 8px;
            }}
        """)
        charts_layout = QHBoxLayout(charts_frame)
        
        self.canvas = FigureCanvas(Figure(figsize=(12, 5), facecolor=COLORS['bg_medium']))
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        charts_layout.addWidget(self.canvas)
        
        layout.addWidget(charts_frame)
        
    def create_stat_card(self, icon, title, value, color_type):
        """Create a modern stat card"""
        card = QFrame()
        
        color_map = {
            'primary': (COLORS['primary'], COLORS['primary_dark']),
            'success': (COLORS['success'], '#16a34a'),
            'error': (COLORS['error'], '#dc2626'),
            'accent': (COLORS['accent'], '#0284c7'),
            'warning': (COLORS['warning'], '#ea580c'),
        }
        
        c1, c2 = color_map.get(color_type, (COLORS['primary'], COLORS['primary_dark']))
        
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c1}, stop:1 {c2});
                border: none;
                border-radius: 12px;
                min-width: 160px;
                max-height: 100px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        
        # Header row
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        header.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            font-size: 11px;
            font-weight: 500;
        """)
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName(f"{title.lower().replace(' ', '_')}_value")
        value_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 700;
        """)
        layout.addWidget(value_label)
        
        # Store reference for updates
        card.value_label = value_label
        
        return card

    def display_results(self, results):
        history = results['history']
        
        # Update stat cards with animation effect
        self.algo_card.value_label.setText(results['algorithm'])
        self.faults_card.value_label.setText(str(results['page_faults']))
        self.hits_card.value_label.setText(str(results['hits']))
        self.ratio_card.value_label.setText(f"{results['hit_ratio']:.1%}")
        
        has_tlb = history[0].get('tlb_hit') is not None if history else False
        
        columns = ['Step', 'Page', 'Frames', 'Status']
        if has_tlb:
            columns.append('TLB')
        columns.append('Working Set')
        
        self.table.setRowCount(len(history))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for i, step in enumerate(history):
            col = 0
            
            # Step number
            step_item = QTableWidgetItem(str(step['step']))
            step_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            step_item.setFont(QFont("Helvetica Neue", 11, QFont.Weight.Bold))
            self.table.setItem(i, col, step_item)
            col += 1
            
            # Page number
            page_item = QTableWidgetItem(str(step['page']))
            page_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            page_item.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
            page_item.setForeground(QBrush(QColor(COLORS['primary_light'])))
            self.table.setItem(i, col, page_item)
            col += 1
            
            # Frames
            frames_text = ' → '.join(str(f) if f is not None else '·' for f in step['frames'])
            frames_item = QTableWidgetItem(frames_text)
            frames_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            frames_item.setFont(QFont("Monaco", 11))
            self.table.setItem(i, col, frames_item)
            col += 1
            
            # Status (Page Fault or Hit)
            if step['page_fault']:
                fault_item = QTableWidgetItem('❌ FAULT')
                fault_item.setForeground(QBrush(QColor(COLORS['error_light'])))
            else:
                fault_item = QTableWidgetItem('✅ HIT')
                fault_item.setForeground(QBrush(QColor(COLORS['success_light'])))
            fault_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            fault_item.setFont(QFont("Helvetica Neue", 10, QFont.Weight.Bold))
            self.table.setItem(i, col, fault_item)
            col += 1
            
            # TLB status
            if has_tlb:
                if step.get('tlb_hit'):
                    tlb_item = QTableWidgetItem('⚡ HIT')
                    tlb_item.setForeground(QBrush(QColor(COLORS['accent'])))
                else:
                    tlb_item = QTableWidgetItem('○ MISS')
                    tlb_item.setForeground(QBrush(QColor(COLORS['text_muted'])))
                tlb_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tlb_item.setFont(QFont("Helvetica Neue", 10))
                self.table.setItem(i, col, tlb_item)
                col += 1
            
            # Working set
            ws_item = QTableWidgetItem(str(step.get('working_set_size', '--')))
            ws_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, col, ws_item)
        
        # Resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.display_chart(results)

    def display_chart(self, results):
        self.canvas.figure.clear()
        self.canvas.figure.set_facecolor(COLORS['bg_medium'])
        
        # Create subplots
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122)
        
        # Style axes
        for ax in [ax1, ax2]:
            ax.set_facecolor(COLORS['bg_light'])
            ax.tick_params(colors=COLORS['text_secondary'])
            ax.spines['bottom'].set_color(COLORS['border'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(COLORS['border'])
        
        # Chart 1: Faults vs Hits
        metrics = ['Page Faults', 'Hits']
        values = [results['page_faults'], results['hits']]
        colors = [COLORS['error'], COLORS['success']]
        
        bars = ax1.bar(metrics, values, color=colors, width=0.6, 
                       edgecolor='white', linewidth=0.5, alpha=0.9)
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val}', ha='center', va='bottom', 
                    fontsize=14, fontweight='bold', color=COLORS['text_primary'])
        
        ax1.set_ylabel('Count', color=COLORS['text_primary'], fontweight='500')
        ax1.set_title(f"{results['algorithm']} Performance", 
                     color=COLORS['text_primary'], fontsize=13, fontweight='600', pad=15)
        ax1.set_ylim(0, max(values) * 1.2)
        
        # Chart 2: Performance metrics or donut chart
        if 'average_access_time' in results:
            # Show access time breakdown
            perf = results['performance_metrics']
            
            # Create a nice info display
            ax2.axis('off')
            
            # Title
            ax2.text(0.5, 0.95, 'Performance Metrics', ha='center', va='top',
                    fontsize=14, fontweight='bold', color=COLORS['text_primary'],
                    transform=ax2.transAxes)
            
            # Metrics
            metrics_text = [
                (f"⏱️ Avg Access Time", f"{results['average_access_time']:,.0f} ns"),
                (f"⚡ TLB Accesses", f"{perf['tlb_accesses']:,}"),
                (f"💾 Disk Accesses", f"{perf['disk_accesses']:,}"),
                (f"📊 Hit Ratio", f"{results['hit_ratio']:.1%}"),
            ]
            
            y_pos = 0.75
            for label, value in metrics_text:
                ax2.text(0.15, y_pos, label, ha='left', va='center',
                        fontsize=11, color=COLORS['text_muted'],
                        transform=ax2.transAxes)
                ax2.text(0.85, y_pos, value, ha='right', va='center',
                        fontsize=12, fontweight='bold', color=COLORS['text_primary'],
                        transform=ax2.transAxes)
                y_pos -= 0.15
        else:
            # Simple donut chart for hit ratio
            hit_ratio = results['hit_ratio']
            fault_ratio = 1 - hit_ratio
            
            sizes = [hit_ratio, fault_ratio]
            colors_pie = [COLORS['success'], COLORS['error']]
            
            wedges, texts = ax2.pie(sizes, colors=colors_pie, startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor=COLORS['bg_medium']))
            
            # Center text
            ax2.text(0, 0, f'{hit_ratio:.0%}', ha='center', va='center',
                    fontsize=20, fontweight='bold', color=COLORS['text_primary'])
            ax2.text(0, -0.15, 'Hit Rate', ha='center', va='center',
                    fontsize=10, color=COLORS['text_muted'])
            
            ax2.set_title('Memory Efficiency', color=COLORS['text_primary'],
                         fontsize=13, fontweight='600', pad=15)
        
        self.canvas.figure.tight_layout(pad=2.0)
        self.canvas.draw()


# Test block to run the widget standalone
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from gui.styles import MAIN_STYLESHEET
    
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLESHEET)
    widget = VisualizationWidget()
    widget.show()
    sys.exit(app.exec())
