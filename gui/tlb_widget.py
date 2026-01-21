"""
Modern TLB Visualization Widget
Beautiful charts and animated stats
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE


class AnimatedStatLabel(QLabel):
    """Label with animated value transitions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        
    def set_value(self, value, suffix=""):
        self._value = value
        self.setText(f"{value}{suffix}")


class TLBVisualizationWidget(QWidget):
    """Widget to visualize TLB performance with modern design"""
    
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
        
        title = QLabel("⚡ TLB Performance Analysis")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Translation Lookaside Buffer - Fast address translation cache")
        subtitle.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_muted']};
        """)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_frame)
        
        # Stats Cards Row
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(16)
        
        self.hits_card = self.create_stat_card("⚡", "TLB Hits", "0", "accent")
        stats_layout.addWidget(self.hits_card)
        
        self.misses_card = self.create_stat_card("○", "TLB Misses", "0", "warning")
        stats_layout.addWidget(self.misses_card)
        
        self.ratio_card = self.create_stat_card("📊", "Hit Ratio", "0%", "success")
        stats_layout.addWidget(self.ratio_card)
        
        self.size_card = self.create_stat_card("📦", "Entries", "0/0", "primary")
        stats_layout.addWidget(self.size_card)
        
        layout.addWidget(stats_frame)
        
        # Charts
        charts_frame = QFrame()
        charts_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setContentsMargins(16, 16, 16, 16)
        
        self.canvas = FigureCanvas(Figure(figsize=(12, 6), facecolor=COLORS['bg_medium']))
        charts_layout.addWidget(self.canvas)
        
        layout.addWidget(charts_frame)
        
        # Info panel
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(14, 165, 168, 0.1);
                border: 1px solid {COLORS['primary']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("💡 About TLB")
        info_title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {COLORS['primary_light']};
        """)
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "The Translation Lookaside Buffer (TLB) is a high-speed cache that stores recent "
            "virtual-to-physical address translations. A TLB hit avoids expensive page table lookups, "
            "significantly improving memory access performance."
        )
        info_text.setStyleSheet(f"""
            font-size: 12px;
            color: {COLORS['text_secondary']};
            line-height: 1.5;
        """)
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
    def create_stat_card(self, icon, title, value, color_type):
        """Create a modern stat card"""
        card = QFrame()
        
        color_map = {
            'primary': (COLORS['primary'], COLORS['primary_dark']),
            'success': (COLORS['success'], '#16a34a'),
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
                min-width: 150px;
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
            font-size: 11px;
            font-weight: 500;
        """)
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 700;
        """)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def display_tlb_stats(self, tlb_stats):
        """Display TLB statistics"""
        if not tlb_stats:
            return
        
        # Update stat cards
        self.hits_card.value_label.setText(str(tlb_stats['hits']))
        self.misses_card.value_label.setText(str(tlb_stats['misses']))
        self.ratio_card.value_label.setText(f"{tlb_stats['hit_ratio']:.1%}")
        self.size_card.value_label.setText(f"{tlb_stats['size']}/{tlb_stats['capacity']}")
        
        self.display_chart(tlb_stats)
    
    def display_chart(self, tlb_stats):
        """Display TLB performance chart"""
        self.canvas.figure.clear()
        self.canvas.figure.set_facecolor(COLORS['bg_medium'])
        
        # Create two subplots
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122)
        
        for ax in [ax1, ax2]:
            ax.set_facecolor(COLORS['bg_light'])
        
        # Donut chart for hit ratio
        hits = tlb_stats['hits']
        misses = tlb_stats['misses']
        
        if hits + misses > 0:
            sizes = [hits, misses]
            colors = [COLORS['accent'], COLORS['warning']]
            labels = ['Hits', 'Misses']
            
            wedges, texts = ax1.pie(sizes, colors=colors, startangle=90,
                                    wedgeprops=dict(width=0.4, edgecolor=COLORS['bg_medium'],
                                                   linewidth=2))
            
            # Center text
            hit_ratio = tlb_stats['hit_ratio']
            ax1.text(0, 0.05, f'{hit_ratio:.0%}', ha='center', va='center',
                    fontsize=28, fontweight='bold', color=COLORS['text_primary'])
            ax1.text(0, -0.15, 'Hit Rate', ha='center', va='center',
                    fontsize=11, color=COLORS['text_muted'])
            
            # Legend
            ax1.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.1),
                      facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                      labelcolor=COLORS['text_primary'], fontsize=10)
        
        ax1.set_title('TLB Hit Distribution', color=COLORS['text_primary'],
                     fontsize=13, fontweight='600', pad=20)
        
        # Bar chart for comparison
        metrics = ['TLB Hits', 'TLB Misses']
        values = [hits, misses]
        colors = [COLORS['accent'], COLORS['warning']]
        
        bars = ax2.bar(metrics, values, color=colors, alpha=0.85,
                      edgecolor='white', linewidth=0.5, width=0.6)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val}', ha='center', va='bottom',
                    fontsize=12, fontweight='bold', color=COLORS['text_primary'])
        
        ax2.set_ylabel('Count', color=COLORS['text_primary'], fontweight='500')
        ax2.set_title('TLB Access Statistics', color=COLORS['text_primary'],
                     fontsize=13, fontweight='600', pad=15)
        ax2.tick_params(colors=COLORS['text_secondary'])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_color(COLORS['border'])
        ax2.spines['left'].set_color(COLORS['border'])
        ax2.grid(axis='y', alpha=0.2, color=COLORS['border'])
        
        self.canvas.figure.tight_layout(pad=2.0)
        self.canvas.draw()
