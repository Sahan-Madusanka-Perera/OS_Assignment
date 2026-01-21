"""
Modern Main Window for Virtual Memory Simulator
Beautiful UI with fluid animations
"""

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QSpinBox, QTextEdit, QComboBox, QMessageBox, 
                             QTabWidget, QCheckBox, QGroupBox, QFileDialog, QFrame, QSizePolicy,
                             QGraphicsDropShadowEffect, QScrollArea)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon, QColor

from gui.styles import MAIN_STYLESHEET, COLORS, INFO_PANEL_STYLE, TITLE_STYLE
from gui.visualization import VisualizationWidget
from gui.comparison_widget import ComparisonWidget
from gui.tlb_widget import TLBVisualizationWidget
from gui.working_set_widget import WorkingSetWidget
from gui.memory_animator import MemoryAnimator
from gui.ml_prediction_widget import MLPredictionWidget
from gui.benchmark_widget import BenchmarkWidget
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm, ClockAlgorithm, LFUAlgorithm
from simulator.simulator import VMSimulator
from simulator.ml_predictor import PredictiveAlgorithm
from utils.exporter import ResultsExporter


class ModernButton(QPushButton):
    """Modern animated button with hover effects"""
    
    def __init__(self, text, icon_text="", variant="primary", parent=None):
        super().__init__(parent)
        self.variant = variant
        
        if icon_text:
            self.setText(f"{icon_text}  {text}")
        else:
            self.setText(text)
            
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(46)
        self.setMinimumWidth(160)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.apply_style()
        
    def apply_style(self):
        styles = {
            'primary': f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
                    color: #ffffff;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.3px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['primary_light']}, stop:1 {COLORS['primary']});
                }}
                QPushButton:pressed {{
                    background: {COLORS['primary_dark']};
                }}
            """,
            'success': f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['success']}, stop:1 #16a34a);
                    color: #ffffff;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.3px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['success_light']}, stop:1 {COLORS['success']});
                }}
            """,
            'secondary': f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['secondary']}, stop:1 #d97706);
                    color: #ffffff;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.3px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {COLORS['secondary_light']}, stop:1 {COLORS['secondary']});
                }}
            """,
            'outline': f"""
                QPushButton {{
                    background: rgba(14, 165, 168, 0.1);
                    color: {COLORS['primary_light']};
                    border: 2px solid {COLORS['primary']};
                    border-radius: 12px;
                    padding: 12px 28px;
                    font-weight: 700;
                    font-size: 14px;
                    letter-spacing: 0.3px;
                }}
                QPushButton:hover {{
                    background: rgba(14, 165, 168, 0.2);
                    border-color: {COLORS['primary_light']};
                    color: #ffffff;
                }}
            """
        }
        self.setStyleSheet(styles.get(self.variant, styles['primary']))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ Virtual Memory Simulator")
        self.last_results = None
        self.last_comparison = None
        self.setup_ui()
        self.apply_styles()
        
    def apply_styles(self):
        self.setStyleSheet(MAIN_STYLESHEET)

    def setup_ui(self):
        # Create main scroll area for entire content
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['bg_dark']};
            }}
        """)
        self.setCentralWidget(main_scroll)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {COLORS['bg_dark']};")
        main_scroll.setWidget(content_widget)
        
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header with title
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Configuration Panel
        config_panel = self.create_config_panel()
        main_layout.addWidget(config_panel)
        
        # Tab Widget with results
        self.tabs = self.create_tabs()
        main_layout.addWidget(self.tabs, 1)  # Stretch factor 1
        
    def create_header(self):
        """Create the application header"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(14, 165, 168, 0.25), 
                    stop:0.5 rgba(245, 158, 11, 0.18),
                    stop:1 rgba(56, 189, 248, 0.2));
                border-radius: 16px;
                padding: 10px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Logo/Icon
        logo_label = QLabel("🧠")
        logo_label.setStyleSheet("font-size: 36px;")
        layout.addWidget(logo_label)
        
        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("Virtual Memory Simulator")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            letter-spacing: -0.5px;
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Explore page replacement algorithms with interactive visualizations")
        subtitle.setStyleSheet(f"""
            font-size: 13px;
            color: {COLORS['text_muted']};
        """)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Version badge
        version_badge = QLabel("v2.0")
        version_badge.setStyleSheet(f"""
            background-color: {COLORS['primary']};
            color: white;
            padding: 6px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 11px;
        """)
        layout.addWidget(version_badge)
        
        return header_frame
        
    def create_config_panel(self):
        """Create the configuration panel"""
        config_group = QGroupBox("⚙️ Simulation Configuration")
        config_layout = QVBoxLayout(config_group)
        config_layout.setSpacing(16)
        
        # First row - Main controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        
        # Frames control
        frames_container = self.create_control_group("🔲 Frames", self.create_frame_spinbox())
        controls_layout.addWidget(frames_container)
        
        # Algorithm control
        algo_container = self.create_control_group("🔄 Algorithm", self.create_algo_combo())
        controls_layout.addWidget(algo_container)
        
        # TLB Size control
        tlb_container = self.create_control_group("⚡ TLB Size", self.create_tlb_spinbox())
        controls_layout.addWidget(tlb_container)
        
        controls_layout.addStretch()
        config_layout.addLayout(controls_layout)
        
        # Options row
        options_layout = QHBoxLayout()
        options_layout.setSpacing(24)
        
        self.tlb_checkbox = QCheckBox("⚡ Enable TLB")
        self.tlb_checkbox.setChecked(True)
        self.tlb_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['accent']};
                font-weight: 600;
                font-size: 13px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['accent']};
                border-color: {COLORS['accent']};
            }}
        """)
        options_layout.addWidget(self.tlb_checkbox)
        
        self.ml_checkbox = QCheckBox("🤖 Enable ML Prediction")
        self.ml_checkbox.setChecked(False)
        self.ml_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['secondary']};
                font-weight: 600;
                font-size: 13px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['secondary']};
                border-color: {COLORS['secondary']};
            }}
        """)
        options_layout.addWidget(self.ml_checkbox)
        
        options_layout.addStretch()
        config_layout.addLayout(options_layout)
        
        # Reference string input
        ref_label = QLabel("📝 Reference String")
        ref_label.setStyleSheet(f"""
            font-weight: 600;
            color: {COLORS['text_primary']};
            font-size: 13px;
        """)
        config_layout.addWidget(ref_label)
        
        self.ref_input = QTextEdit()
        self.ref_input.setMaximumHeight(120)
        self.ref_input.setMinimumHeight(90)
        self.ref_input.setPlaceholderText("Enter page reference sequence (comma-separated): e.g., 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")
        self.ref_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['bg_light']};
                border: 2px solid {COLORS['border']};
                border-radius: 12px;
                padding: 14px 16px;
                color: {COLORS['text_primary']};
                font-size: 15px;
                font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
                line-height: 1.5;
            }}
            QTextEdit:focus {{
                border-color: {COLORS['primary']};
                background-color: rgba(14, 165, 168, 0.08);
            }}
        """)
        config_layout.addWidget(self.ref_input)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.run_button = ModernButton("Run Simulation", "▶️", "primary")
        self.run_button.clicked.connect(self.run_simulation)
        buttons_layout.addWidget(self.run_button)
        
        self.compare_button = ModernButton("Compare All", "📊", "success")
        self.compare_button.clicked.connect(self.compare_algorithms)
        buttons_layout.addWidget(self.compare_button)
        
        self.export_button = ModernButton("Export", "💾", "outline")
        self.export_button.clicked.connect(self.export_results)
        buttons_layout.addWidget(self.export_button)
        
        buttons_layout.addStretch()
        config_layout.addLayout(buttons_layout)
        
        return config_group
        
    def create_control_group(self, label_text, widget):
        """Create a labeled control group"""
        container = QFrame()
        container.setMinimumWidth(140)
        container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: 12px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        layout.addWidget(label)
        layout.addWidget(widget)
        
        return container
        
    def create_frame_spinbox(self):
        self.frame_count_spinbox = QSpinBox()
        self.frame_count_spinbox.setRange(1, 10)
        self.frame_count_spinbox.setValue(3)
        self.frame_count_spinbox.setMinimumWidth(100)
        self.frame_count_spinbox.setMinimumHeight(40)
        return self.frame_count_spinbox
        
    def create_algo_combo(self):
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["FIFO", "LRU", "LFU", "Optimal", "Clock"])
        self.algo_combo.setMinimumWidth(150)
        self.algo_combo.setMinimumHeight(40)
        return self.algo_combo
        
    def create_tlb_spinbox(self):
        self.tlb_size_spinbox = QSpinBox()
        self.tlb_size_spinbox.setRange(2, 16)
        self.tlb_size_spinbox.setValue(4)
        self.tlb_size_spinbox.setMinimumWidth(100)
        self.tlb_size_spinbox.setMinimumHeight(40)
        return self.tlb_size_spinbox
        
    def create_tabs(self):
        """Create the tabbed results panel"""
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        
        # Add tabs with icons - no individual scroll, main window scrolls
        self.results_widget = VisualizationWidget()
        tabs.addTab(self.results_widget, "📈 Results")
        
        self.comparison_widget = ComparisonWidget()
        tabs.addTab(self.comparison_widget, "⚖️ Comparison")
        
        self.benchmark_widget = BenchmarkWidget()
        tabs.addTab(self.benchmark_widget, "📊 Benchmarks")
        
        self.ml_widget = MLPredictionWidget()
        tabs.addTab(self.ml_widget, "🤖 ML Analysis")
        
        self.tlb_widget = TLBVisualizationWidget()
        tabs.addTab(self.tlb_widget, "⚡ TLB")
        
        self.working_set_widget = WorkingSetWidget()
        tabs.addTab(self.working_set_widget, "📦 Working Set")
        
        self.animator_widget = MemoryAnimator()
        tabs.addTab(self.animator_widget, "🎬 Animation")
        
        return tabs

    def run_simulation(self):
        try:
            ref_string_text = self.ref_input.toPlainText().strip()
            if not ref_string_text:
                QMessageBox.warning(self, "Input Error", "Please enter a reference string.")
                return
            
            reference_string = [int(x.strip()) for x in ref_string_text.split(',')]
            
            num_frames = self.frame_count_spinbox.value()
            algo_name = self.algo_combo.currentText()
            use_tlb = self.tlb_checkbox.isChecked()
            tlb_size = self.tlb_size_spinbox.value()
            use_ml = self.ml_checkbox.isChecked()
            
            algorithm_classes = {
                'FIFO': FIFOAlgorithm,
                'LRU': LRUAlgorithm,
                'LFU': LFUAlgorithm,
                'Optimal': OptimalAlgorithm,
                'Clock': ClockAlgorithm
            }

            algorithm = algorithm_classes[algo_name](num_frames)
            
            if algo_name == 'Optimal':
                algorithm.set_reference_string(reference_string)
            
            if use_ml:
                base_algo = algorithm_classes[algo_name](num_frames)
                if algo_name == 'Optimal':
                    base_algo.set_reference_string(reference_string)
                
                base_simulator = VMSimulator(reference_string, num_frames, base_algo,
                                           use_tlb=use_tlb, tlb_size=tlb_size)
                base_results = base_simulator.run()
                
                ml_algorithm = PredictiveAlgorithm(algorithm_classes[algo_name](num_frames))
                if algo_name == 'Optimal':
                    ml_algorithm.base_algorithm.set_reference_string(reference_string)
                
                simulator = VMSimulator(reference_string, num_frames, ml_algorithm,
                                      use_tlb=use_tlb, tlb_size=tlb_size)
                results = simulator.run()
                results['ml_prediction_stats'] = ml_algorithm.get_prediction_stats()
                
                self.ml_widget.display_ml_comparison(base_results, results)
                self.tabs.setCurrentIndex(3)  # ML Analysis tab
            else:
                simulator = VMSimulator(reference_string, num_frames, algorithm, 
                                       use_tlb=use_tlb, tlb_size=tlb_size)
                results = simulator.run()
                self.tabs.setCurrentIndex(0)
            
            self.last_results = results
            self.results_widget.display_results(results)
            
            self.animator_widget.load_results(results)
            
            if use_tlb and 'tlb_stats' in results:
                self.tlb_widget.display_tlb_stats(results['tlb_stats'])
            
            if 'working_set_stats' in results:
                self.working_set_widget.display_working_set_stats(
                    results['working_set_stats'], num_frames)
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid comma-separated integers.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def compare_algorithms(self):
        try:
            ref_string_text = self.ref_input.toPlainText().strip()
            if not ref_string_text:
                QMessageBox.warning(self, "Input Error", "Please enter a reference string.")
                return
            
            reference_string = [int(x.strip()) for x in ref_string_text.split(',')]
            num_frames = self.frame_count_spinbox.value()
            use_tlb = self.tlb_checkbox.isChecked()
            
            self.tabs.setCurrentIndex(1)
            results = self.comparison_widget.compare_algorithms(reference_string, num_frames, use_tlb)
            self.last_comparison = results
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid comma-separated integers.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def export_results(self):
        """Export simulation results to file"""
        if not self.last_results and not self.last_comparison:
            QMessageBox.warning(self, "No Data", "Please run a simulation first before exporting.")
            return
        
        file_filter = "CSV Files (*.csv);;JSON Files (*.json);;Text Files (*.txt)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Results", "", file_filter
        )
        
        if not filename:
            return
        
        try:
            exporter = ResultsExporter()
            
            if self.last_comparison and self.tabs.currentIndex() == 1:
                if filename.endswith('.csv'):
                    exporter.export_comparison_to_csv(self.last_comparison, filename)
                elif filename.endswith('.json'):
                    export_data = {name: result for name, result in self.last_comparison}
                    exporter.export_to_json({'comparison': export_data}, filename)
                else:
                    filename = filename + '.csv'
                    exporter.export_comparison_to_csv(self.last_comparison, filename)
            
            elif self.last_results:
                if filename.endswith('.csv'):
                    exporter.export_to_csv(self.last_results, filename)
                elif filename.endswith('.json'):
                    exporter.export_to_json(self.last_results, filename)
                elif filename.endswith('.txt'):
                    exporter.export_summary_report(self.last_results, filename)
                else:
                    filename = filename + '.csv'
                    exporter.export_to_csv(self.last_results, filename)
            
            QMessageBox.information(self, "Export Successful", f"Results exported to:\n{filename}")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export results:\n{str(e)}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
