from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VisualizationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Step-by-step Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Chart Comparison
        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)

    def display_results(self, results):
        history = results['history']
        
        has_tlb = history[0].get('tlb_hit') is not None if history else False
        
        columns = ['Step', 'Page', 'Frames', 'Page Fault']
        if has_tlb:
            columns.append('TLB Hit')
        columns.append('Working Set')
        
        self.table.setRowCount(len(history))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for i, step in enumerate(history):
            col = 0
            self.table.setItem(i, col, QTableWidgetItem(str(step['step'])))
            col += 1
            self.table.setItem(i, col, QTableWidgetItem(str(step['page'])))
            col += 1
            self.table.setItem(i, col, QTableWidgetItem(str(step['frames'])))
            col += 1
            
            fault_item = QTableWidgetItem('Yes' if step['page_fault'] else 'No')
            if step['page_fault']:
                fault_item.setBackground(Qt.GlobalColor.red)
            else:
                fault_item.setBackground(Qt.GlobalColor.green)
            self.table.setItem(i, col, fault_item)
            col += 1
            
            if has_tlb:
                tlb_item = QTableWidgetItem('Yes' if step.get('tlb_hit') else 'No')
                if step.get('tlb_hit'):
                    tlb_item.setBackground(Qt.GlobalColor.green)
                self.table.setItem(i, col, tlb_item)
                col += 1
            
            self.table.setItem(i, col, QTableWidgetItem(str(step.get('working_set_size', '--'))))
        
        self.table.resizeColumnsToContents()
        
        self.display_chart(results)

    def display_chart(self, results):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        metrics = ['Page Faults', 'Hits']
        values = [results['page_faults'], results['hits']]
        colors = ['#ff6b6b', '#51cf66']
        
        ax.bar(metrics, values, color=colors)
        ax.set_ylabel('Count')
        ax.set_title(f"{results['algorithm']} - Hit Ratio: {results['hit_ratio']:.2%}")
        ax.grid(axis='y', alpha=0.3)
        
        self.canvas.draw()


# Test block to run the widget standalone
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = VisualizationWidget()
    widget.show()
    sys.exit(app.exec())
