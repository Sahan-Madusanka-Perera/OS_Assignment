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
        ax1 = self.canvas.figure.add_subplot(121)
        ax2 = self.canvas.figure.add_subplot(122)
        
        metrics = ['Page Faults', 'Hits']
        values = [results['page_faults'], results['hits']]
        colors = ['#ff6b6b', '#51cf66']
        
        ax1.bar(metrics, values, color=colors)
        ax1.set_ylabel('Count')
        ax1.set_title(f"{results['algorithm']} - Hit Ratio: {results['hit_ratio']:.2%}")
        ax1.grid(axis='y', alpha=0.3)
        
        if 'average_access_time' in results:
            avg_time_ns = results['average_access_time']
            perf = results['performance_metrics']
            
            ax2.text(0.5, 0.9, f"Average Access Time", ha='center', va='top', fontsize=10, weight='bold', transform=ax2.transAxes)
            ax2.text(0.5, 0.75, f"{avg_time_ns:,.0f} ns", ha='center', va='top', fontsize=12, transform=ax2.transAxes)
            ax2.text(0.5, 0.60, f"({avg_time_ns/1000:,.2f} µs)", ha='center', va='top', fontsize=9, transform=ax2.transAxes)
            
            ax2.text(0.5, 0.45, f"TLB: {perf['tlb_accesses']:,}", ha='center', va='top', fontsize=8, transform=ax2.transAxes)
            ax2.text(0.5, 0.35, f"Disk: {perf['disk_accesses']:,}", ha='center', va='top', fontsize=8, transform=ax2.transAxes)
            ax2.text(0.5, 0.25, f"Total: {perf['total_time_ms']:,.2f} ms", ha='center', va='top', fontsize=8, transform=ax2.transAxes)
            
            ax2.axis('off')
        
        self.canvas.figure.tight_layout()
        self.canvas.draw()


# Test block to run the widget standalone
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = VisualizationWidget()
    widget.show()
    sys.exit(app.exec())
