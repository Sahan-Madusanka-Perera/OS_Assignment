"""
Modern UI Styles and Themes for Virtual Memory Simulator
Beautiful glassmorphism-inspired design with smooth animations
"""

# Modern color palette
COLORS = {
    'primary': '#0ea5a8',          # Teal
    'primary_light': '#22d3ee',
    'primary_dark': '#0f766e',
    'secondary': '#f59e0b',         # Amber
    'secondary_light': '#fbbf24',
    'accent': '#38bdf8',            # Sky
    'success': '#22c55e',           # Green
    'success_light': '#4ade80',
    'warning': '#f97316',           # Orange
    'warning_light': '#fdba74',
    'error': '#ef4444',             # Red
    'error_light': '#f87171',
    
    # Neutrals
    'bg_dark': '#0b111a',
    'bg_medium': '#111827',
    'bg_light': '#1f2937',
    'bg_card': '#111827',
    'surface': '#1c2533',
    'border': '#334155',
    'border_light': '#475569',
    
    # Text
    'text_primary': '#f8fafc',      # Slate 50
    'text_secondary': '#cbd5e1',
    'text_muted': '#94a3b8',
}

# Main application stylesheet
MAIN_STYLESHEET = f"""
/* ===== Global Styles ===== */
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Space Grotesk', 'IBM Plex Sans', 'Noto Sans', sans-serif;
    font-size: 13px;
}}

/* ===== Group Boxes ===== */
QGroupBox {{
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 16px;
    padding: 20px 16px 16px 16px;
    font-weight: 600;
    font-size: 14px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 4px;
    padding: 4px 12px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
    border-radius: 6px;
    color: {COLORS['text_primary']};
}}

/* ===== Buttons ===== */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 700;
    font-size: 14px;
    min-width: 120px;
    min-height: 40px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['primary_light']}, stop:1 {COLORS['primary']});
}}

QPushButton:pressed {{
    background: {COLORS['primary_dark']};
}}

QPushButton:disabled {{
    background: {COLORS['bg_light']};
    color: {COLORS['text_muted']};
}}

/* Special Button Variants */
QPushButton[class="success"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['success']}, stop:1 #16a34a);
}}

QPushButton[class="warning"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['warning']}, stop:1 #ea580c);
}}

QPushButton[class="danger"] {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['error']}, stop:1 #dc2626);
}}

/* ===== Input Fields ===== */
QLineEdit, QTextEdit, QSpinBox, QComboBox {{
    background-color: {COLORS['bg_light']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['primary']};
    font-size: 14px;
    min-height: 20px;
}}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border-color: {COLORS['primary']};
    background-color: {COLORS['bg_medium']};
}}

QTextEdit {{
    border-radius: 10px;
    padding: 12px;
}}

QLineEdit[placeholderText], QTextEdit[placeholderText] {{
    color: {COLORS['text_muted']};
}}

/* SpinBox specific */
QSpinBox {{
    min-width: 100px;
    min-height: 36px;
    padding-right: 30px;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {COLORS['primary']};
    border: none;
    border-radius: 4px;
    width: 24px;
    height: 16px;
    margin: 2px 4px;
}}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background-color: {COLORS['primary_light']};
}}

QSpinBox::up-arrow {{
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 6px solid #ffffff;
}}

QSpinBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #ffffff;
}}

/* ComboBox specific */
QComboBox {{
    min-width: 140px;
    min-height: 36px;
    padding-right: 30px;
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
    subcontrol-position: right center;
}}

QComboBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 7px solid #ffffff;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_medium']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['primary']};
    selection-color: #ffffff;
    padding: 6px;
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    min-height: 32px;
    padding: 6px 12px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {COLORS['primary']};
}}

/* ===== Labels ===== */
QLabel {{
    color: {COLORS['text_primary']};
    font-size: 13px;
}}

QLabel[class="title"] {{
    font-size: 20px;
    font-weight: 700;
    color: {COLORS['text_primary']};
}}

QLabel[class="subtitle"] {{
    font-size: 12px;
    color: {COLORS['text_muted']};
    font-style: italic;
}}

/* ===== Tab Widget ===== */
QTabWidget::pane {{
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    border-top-left-radius: 0px;
    padding: 12px;
}}

QTabBar {{
    qproperty-drawBase: 0;
}}

QTabBar::tab {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text_secondary']};
    border: none;
    padding: 14px 20px;
    margin-right: 6px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: 600;
    font-size: 13px;
    min-width: 80px;
}}

QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
    color: #ffffff;
    font-weight: 700;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
}}

/* ===== Tables ===== */
QTableWidget, QTableView {{
    background-color: {COLORS['bg_medium']};
    alternate-background-color: {COLORS['bg_light']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['primary']};
    selection-color: {COLORS['text_primary']};
}}

QTableWidget::item, QTableView::item {{
    padding: 8px;
    border-bottom: 1px solid {COLORS['border']};
}}

QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {COLORS['primary']};
}}

QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['bg_light']}, stop:1 {COLORS['bg_medium']});
    color: {COLORS['text_primary']};
    padding: 10px 8px;
    border: none;
    border-bottom: 2px solid {COLORS['primary']};
    font-weight: 600;
    font-size: 12px;
}}

QHeaderView::section:first {{
    border-top-left-radius: 8px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 8px;
}}

/* ===== Checkboxes ===== */
QCheckBox {{
    spacing: 10px;
    color: {COLORS['text_primary']};
    font-size: 13px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    background-color: {COLORS['bg_light']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['primary']};
    border-color: {COLORS['primary']};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS['primary_light']};
}}

/* ===== Sliders ===== */
QSlider::groove:horizontal {{
    background: {COLORS['bg_light']};
    height: 8px;
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
    width: 20px;
    height: 20px;
    margin: -6px 0;
    border-radius: 10px;
    border: 2px solid {COLORS['text_primary']};
}}

QSlider::handle:horizontal:hover {{
    background: {COLORS['primary_light']};
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
    border-radius: 4px;
}}

/* ===== ScrollBars ===== */
QScrollBar:vertical {{
    background: {COLORS['bg_medium']};
    width: 14px;
    border-radius: 7px;
    margin: 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['border_light']};
    min-height: 40px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['primary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: {COLORS['bg_medium']};
    height: 14px;
    border-radius: 7px;
    margin: 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['border_light']};
    min-width: 40px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS['primary']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ===== Message Boxes ===== */
QMessageBox {{
    background-color: {COLORS['bg_medium']};
}}

QMessageBox QLabel {{
    color: {COLORS['text_primary']};
    font-size: 13px;
}}

QMessageBox QPushButton {{
    min-width: 80px;
    padding: 8px 16px;
}}

/* ===== Tool Tips ===== */
QToolTip {{
    background-color: {COLORS['bg_medium']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['primary']};
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
}}

/* ===== Progress Bar ===== */
QProgressBar {{
    background-color: {COLORS['bg_light']};
    border: none;
    border-radius: 8px;
    text-align: center;
    color: {COLORS['text_primary']};
    font-weight: 600;
    height: 20px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
    border-radius: 8px;
}}
"""

# Card-style widget stylesheet
CARD_STYLE = f"""
    background-color: {COLORS['bg_medium']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 16px;
"""

# Stats card styles
STATS_CARD_PRIMARY = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

STATS_CARD_SUCCESS = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['success']}, stop:1 #16a34a);
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

STATS_CARD_WARNING = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['warning']}, stop:1 #ea580c);
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

STATS_CARD_ERROR = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['error']}, stop:1 #dc2626);
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

STATS_CARD_ACCENT = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['accent']}, stop:1 #0284c7);
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

STATS_CARD_SECONDARY = f"""
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['secondary']}, stop:1 #d97706);
    border: none;
    border-radius: 12px;
    padding: 16px;
    color: {COLORS['text_primary']};
"""

# Info panel styles  
INFO_PANEL_STYLE = f"""
    background-color: rgba(14, 165, 168, 0.15);
    border: 1px solid {COLORS['primary']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {COLORS['text_primary']};
    font-size: 13px;
"""

WARNING_PANEL_STYLE = f"""
    background-color: rgba(249, 115, 22, 0.15);
    border: 1px solid {COLORS['warning']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {COLORS['warning_light']};
    font-size: 13px;
"""

SUCCESS_PANEL_STYLE = f"""
    background-color: rgba(34, 197, 94, 0.15);
    border: 1px solid {COLORS['success']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {COLORS['success_light']};
    font-size: 13px;
"""

ERROR_PANEL_STYLE = f"""
    background-color: rgba(239, 68, 68, 0.15);
    border: 1px solid {COLORS['error']};
    border-radius: 10px;
    padding: 12px 16px;
    color: {COLORS['error_light']};
    font-size: 13px;
"""

# Title styles
TITLE_STYLE = f"""
    font-size: 22px;
    font-weight: 700;
    color: {COLORS['text_primary']};
    padding: 8px 0;
"""

SUBTITLE_STYLE = f"""
    font-size: 12px;
    color: {COLORS['text_muted']};
    font-style: italic;
    padding-bottom: 8px;
"""

# Matplotlib style for dark theme
MATPLOTLIB_STYLE = {
    'figure.facecolor': COLORS['bg_medium'],
    'axes.facecolor': COLORS['bg_light'],
    'axes.edgecolor': COLORS['border'],
    'axes.labelcolor': COLORS['text_primary'],
    'axes.titlecolor': COLORS['text_primary'],
    'xtick.color': COLORS['text_secondary'],
    'ytick.color': COLORS['text_secondary'],
    'text.color': COLORS['text_primary'],
    'grid.color': COLORS['border'],
    'grid.alpha': 0.3,
    'legend.facecolor': COLORS['bg_medium'],
    'legend.edgecolor': COLORS['border'],
    'legend.labelcolor': COLORS['text_primary'],
}

# Chart colors
CHART_COLORS = [
    '#0ea5a8',
    '#f59e0b',
    '#38bdf8',
    '#22c55e',
    '#f97316',
    '#ef4444',
    '#a3e635',
    '#fb7185',
]

GRADIENT_COLORS = {
    'primary': ['#0ea5a8', '#0f766e'],
    'success': ['#22c55e', '#16a34a'],
    'warning': ['#f97316', '#ea580c'],
    'error': ['#ef4444', '#dc2626'],
    'secondary': ['#f59e0b', '#d97706'],
    'accent': ['#38bdf8', '#0284c7'],
}
