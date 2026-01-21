import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.styles import MAIN_STYLESHEET

def main():
    """Entry point for the Virtual Memory Simulator application"""
    app = QApplication(sys.argv)
    
    # Apply modern dark theme stylesheet
    app.setStyleSheet(MAIN_STYLESHEET)
    
    window = MainWindow()
    window.resize(1280, 900)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
