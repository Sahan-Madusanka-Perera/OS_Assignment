from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QSpinBox, QTextEdit, QComboBox, QMessageBox, 
                             QTabWidget, QCheckBox, QGroupBox, QFileDialog)
from gui.visualization import VisualizationWidget
from gui.comparison_widget import ComparisonWidget
from gui.tlb_widget import TLBVisualizationWidget
from gui.working_set_widget import WorkingSetWidget
from gui.memory_animator import MemoryAnimator
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, OptimalAlgorithm, ClockAlgorithm, LFUAlgorithm
from simulator.simulator import VMSimulator
from utils.exporter import ResultsExporter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Memory Simulator")
        self.last_results = None
        self.last_comparison = None
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        input_group = QGroupBox("Simulation Configuration")
        input_layout = QVBoxLayout()

        controls_layout = QHBoxLayout()
        
        controls_layout.addWidget(QLabel("Number of Frames:"))
        self.frame_count_spinbox = QSpinBox()
        self.frame_count_spinbox.setRange(1, 10)
        self.frame_count_spinbox.setValue(3)
        controls_layout.addWidget(self.frame_count_spinbox)

        controls_layout.addWidget(QLabel("Algorithm:"))
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["FIFO", "LRU", "LFU", "Optimal", "Clock"])
        controls_layout.addWidget(self.algo_combo)
        
        controls_layout.addWidget(QLabel("TLB Size:"))
        self.tlb_size_spinbox = QSpinBox()
        self.tlb_size_spinbox.setRange(2, 16)
        self.tlb_size_spinbox.setValue(4)
        controls_layout.addWidget(self.tlb_size_spinbox)

        input_layout.addLayout(controls_layout)

        options_layout = QHBoxLayout()
        self.tlb_checkbox = QCheckBox("Enable TLB")
        self.tlb_checkbox.setChecked(True)
        options_layout.addWidget(self.tlb_checkbox)
        options_layout.addStretch()
        
        input_layout.addLayout(options_layout)

        input_layout.addWidget(QLabel("Reference String (comma-separated):"))
        self.ref_input = QTextEdit()
        self.ref_input.setMaximumHeight(60)
        self.ref_input.setPlaceholderText("e.g., 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")
        input_layout.addWidget(self.ref_input)

        buttons_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Single Algorithm")
        self.run_button.clicked.connect(self.run_simulation)
        buttons_layout.addWidget(self.run_button)
        
        self.compare_button = QPushButton("Compare All Algorithms")
        self.compare_button.clicked.connect(self.compare_algorithms)
        buttons_layout.addWidget(self.compare_button)
        
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        buttons_layout.addWidget(self.export_button)
        
        input_layout.addLayout(buttons_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        self.tabs = QTabWidget()
        
        self.results_widget = VisualizationWidget()
        self.tabs.addTab(self.results_widget, "Single Algorithm Results")
        
        self.comparison_widget = ComparisonWidget()
        self.tabs.addTab(self.comparison_widget, "Algorithm Comparison")
        
        self.tlb_widget = TLBVisualizationWidget()
        self.tabs.addTab(self.tlb_widget, "TLB Analysis")
        
        self.working_set_widget = WorkingSetWidget()
        self.tabs.addTab(self.working_set_widget, "Working Set & Thrashing")
        
        self.animator_widget = MemoryAnimator()
        self.tabs.addTab(self.animator_widget, "Animation")
        
        layout.addWidget(self.tabs)

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
            
            algorithm_map = {
                'FIFO': FIFOAlgorithm(num_frames),
                'LRU': LRUAlgorithm(num_frames),
                'LFU': LFUAlgorithm(num_frames),
                'Optimal': OptimalAlgorithm(num_frames),
                'Clock': ClockAlgorithm(num_frames)
            }
            
            algorithm = algorithm_map[algo_name]
            
            if algo_name == 'Optimal':
                algorithm.set_reference_string(reference_string)
            
            simulator = VMSimulator(reference_string, num_frames, algorithm, 
                                   use_tlb=use_tlb, tlb_size=tlb_size)
            results = simulator.run()
            self.last_results = results
            
            self.tabs.setCurrentIndex(0)
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
