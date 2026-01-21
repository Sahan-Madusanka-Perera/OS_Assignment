"""
Modern Working Set Widget
Visualize working set size and detect thrashing
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from gui.styles import COLORS, MATPLOTLIB_STYLE


class WorkingSetWidget(QWidget):
    """Widget to visualize working set and detect thrashing"""
    
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
        
        title = QLabel("📦 Working Set Analysis")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Monitor memory usage patterns and detect thrashing conditions")
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
        
        self.ws_card = self.create_stat_card("📦", "Working Set", "0", "primary")
        stats_layout.addWidget(self.ws_card)
        
        self.fault_rate_card = self.create_stat_card("📈", "Fault Rate", "0%", "warning")
        stats_layout.addWidget(self.fault_rate_card)
        
        self.status_card = self.create_stat_card("🔍", "Status", "N/A", "success")
        stats_layout.addWidget(self.status_card)
        
        layout.addWidget(stats_frame)
        
        # Warning panel (hidden by default)
        self.warning_frame = QFrame()
        self.warning_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(239, 68, 68, 0.15);
                border: 2px solid {COLORS['error']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        self.warning_frame.hide()
        
        warning_layout = QHBoxLayout(self.warning_frame)
        
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("font-size: 32px;")
        warning_layout.addWidget(warning_icon)
        
        warning_content = QVBoxLayout()
        
        self.warning_title = QLabel("Thrashing Detected!")
        self.warning_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 700;
            color: {COLORS['error']};
        """)
        warning_content.addWidget(self.warning_title)
        
        self.warning_text = QLabel()
        self.warning_text.setStyleSheet(f"""
            font-size: 13px;
            color: {COLORS['text_secondary']};
            line-height: 1.4;
        """)
        self.warning_text.setWordWrap(True)
        warning_content.addWidget(self.warning_text)
        
        warning_layout.addLayout(warning_content, 1)
        layout.addWidget(self.warning_frame)
        
        # Chart
        chart_label = QLabel("📊 Working Set Size Over Time")
        chart_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding: 8px 0;
        """)
        layout.addWidget(chart_label)
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(8, 8, 8, 8)
        
        self.canvas = FigureCanvas(Figure(figsize=(12, 6), facecolor=COLORS['bg_medium']))
        chart_layout.addWidget(self.canvas)
        
        layout.addWidget(chart_frame)
        
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
        
        info_title = QLabel("💡 About Working Set & Thrashing")
        info_title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {COLORS['primary_light']};
        """)
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "The Working Set is the set of pages a process is actively using. "
            "When the working set exceeds available frames, thrashing occurs - "
            "the system spends more time paging than executing, severely degrading performance."
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
            'warning': (COLORS['warning'], '#ea580c'),
            'error': (COLORS['error'], '#dc2626'),
        }
        
        c1, c2 = color_map.get(color_type, (COLORS['primary'], COLORS['primary_dark']))
        
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c1}, stop:1 {c2});
                border: none;
                border-radius: 12px;
                min-width: 180px;
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
    
    def display_working_set_stats(self, ws_stats, num_frames):
        """Display working set statistics"""
        if not ws_stats:
            return
        
        # Update stat cards
        self.ws_card.value_label.setText(str(ws_stats['current_working_set']))
        self.fault_rate_card.value_label.setText(f"{ws_stats['fault_rate']:.1%}")
        
        # Update status and show/hide warning
        if ws_stats['is_thrashing']:
            self.status_card.value_label.setText("⚠️ THRASHING")
            
            # Update status card color
            self.status_card.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['error']}, stop:1 #dc2626);
                    border: none;
                    border-radius: 12px;
                    min-width: 180px;
                }}
            """)
            
            # Show warning
            self.warning_text.setText(
                f"Working set size ({ws_stats['current_working_set']}) exceeds available frames ({num_frames}).\n"
                f"Recommendation: Increase memory frames or reduce working set to improve performance."
            )
            self.warning_frame.show()
        else:
            self.status_card.value_label.setText("✅ Normal")
            
            # Update status card color
            self.status_card.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['success']}, stop:1 #16a34a);
                    border: none;
                    border-radius: 12px;
                    min-width: 180px;
                }}
            """)
            self.warning_frame.hide()
        
        self.display_chart(ws_stats, num_frames)
    
    def display_chart(self, ws_stats, num_frames):
        """Display working set size over time"""
        self.canvas.figure.clear()
        self.canvas.figure.set_facecolor(COLORS['bg_medium'])
        ax = self.canvas.figure.add_subplot(111)
        ax.set_facecolor(COLORS['bg_light'])
        
        history = ws_stats['working_set_history']
        if not history:
            return
        
        steps = list(range(1, len(history) + 1))
        
        # Main line
        ax.plot(steps, history, color=COLORS['primary'], linewidth=2.5, 
               label='Working Set Size', marker='o', markersize=4, alpha=0.9)
        
        # Frame limit line
        ax.axhline(y=num_frames, color=COLORS['error'], linestyle='--', 
                  linewidth=2, label=f'Available Frames ({num_frames})', alpha=0.8)
        
        # Fill thrashing regions
        if ws_stats['is_thrashing']:
            ax.fill_between(steps, history, num_frames,
                           where=[h > num_frames for h in history],
                           color=COLORS['error'], alpha=0.2, label='Thrashing Region')
            
            # Fill normal regions
            ax.fill_between(steps, history, 0,
                           where=[h <= num_frames for h in history],
                           color=COLORS['success'], alpha=0.1)
        else:
            ax.fill_between(steps, history, 0, color=COLORS['success'], alpha=0.1)
        
        ax.set_xlabel('Access Step', color=COLORS['text_primary'], fontweight='500')
        ax.set_ylabel('Working Set Size', color=COLORS['text_primary'], fontweight='500')
        ax.set_title('Working Set Size Over Time', color=COLORS['text_primary'],
                    fontsize=13, fontweight='600', pad=15)
        
        ax.legend(facecolor=COLORS['bg_medium'], edgecolor=COLORS['border'],
                 labelcolor=COLORS['text_primary'], loc='upper right')
        
        ax.tick_params(colors=COLORS['text_secondary'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.spines['left'].set_color(COLORS['border'])
        ax.grid(True, alpha=0.2, color=COLORS['border'])
        
        # Set y-axis to start from 0
        ax.set_ylim(bottom=0)
        
        self.canvas.figure.tight_layout()
        self.canvas.draw()
