from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

class MemoryAnimator(QWidget):
    """Animate memory frame allocation step-by-step"""
    
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_step = 0
        self.is_playing = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Memory Frame Animation")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        self.canvas = FigureCanvas(Figure(figsize=(10, 4)))
        layout.addWidget(self.canvas)
        
        self.info_label = QLabel()
        self.info_label.setStyleSheet("font-size: 12px; padding: 8px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(self.info_label)
        
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)
        
        self.step_button = QPushButton("Next Step")
        self.step_button.clicked.connect(self.next_step)
        controls_layout.addWidget(self.step_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        controls_layout.addWidget(self.reset_button)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_changed)
        controls_layout.addWidget(self.slider)
        
        self.step_label = QLabel("Step: 0/0")
        controls_layout.addWidget(self.step_label)
        
        layout.addLayout(controls_layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        
    def load_results(self, results):
        """Load simulation results for animation"""
        self.history = results.get('history', [])
        self.current_step = 0
        self.slider.setMaximum(len(self.history) - 1 if self.history else 0)
        self.slider.setValue(0)
        self.update_display()
        
    def toggle_play(self):
        """Toggle animation playback"""
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText("Play")
            self.is_playing = False
        else:
            self.timer.start(800)
            self.play_button.setText("Pause")
            self.is_playing = True
            
    def next_step(self):
        """Advance to next step"""
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.slider.setValue(self.current_step)
            self.update_display()
        else:
            if self.is_playing:
                self.toggle_play()
                
    def reset(self):
        """Reset to beginning"""
        if self.is_playing:
            self.toggle_play()
        self.current_step = 0
        self.slider.setValue(0)
        self.update_display()
        
    def slider_changed(self, value):
        """Handle slider movement"""
        self.current_step = value
        self.update_display()
        
    def update_display(self):
        """Update the visual display"""
        if not self.history or self.current_step >= len(self.history):
            return
            
        step_data = self.history[self.current_step]
        
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        
        frames = step_data.get('frames', [])
        page = step_data.get('page')
        page_fault = step_data.get('page_fault', False)
        tlb_hit = step_data.get('tlb_hit')
        
        num_frames = len(frames) if frames else 3
        frame_width = 0.8
        frame_height = 0.6
        spacing = 1.0
        
        for i in range(num_frames):
            x = i * spacing
            y = 0
            
            if i < len(frames) and frames[i] is not None:
                color = '#90EE90' if frames[i] == page else '#E0E0E0'
                rect = patches.Rectangle((x, y), frame_width, frame_height,
                                        linewidth=2, edgecolor='black',
                                        facecolor=color)
                ax.add_patch(rect)
                ax.text(x + frame_width/2, y + frame_height/2, str(frames[i]),
                       ha='center', va='center', fontsize=16, weight='bold')
            else:
                rect = patches.Rectangle((x, y), frame_width, frame_height,
                                        linewidth=2, edgecolor='gray',
                                        facecolor='white', linestyle='--')
                ax.add_patch(rect)
                ax.text(x + frame_width/2, y + frame_height/2, 'Empty',
                       ha='center', va='center', fontsize=10, style='italic', color='gray')
            
            ax.text(x + frame_width/2, y - 0.15, f'Frame {i}',
                   ha='center', va='top', fontsize=9)
        
        page_x = num_frames * spacing + 0.5
        page_color = '#FF6B6B' if page_fault else '#51CF66'
        circle = patches.Circle((page_x + 0.4, 0.3), 0.25,
                               facecolor=page_color, edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(page_x + 0.4, 0.3, str(page),
               ha='center', va='center', fontsize=14, weight='bold', color='white')
        ax.text(page_x + 0.4, -0.15, 'Incoming\nPage',
               ha='center', va='top', fontsize=9)
        
        ax.arrow(page_x + 0.15, 0.3, -0.5, 0,
                head_width=0.1, head_length=0.15, fc=page_color, ec=page_color, linewidth=2)
        
        ax.set_xlim(-0.2, page_x + 1.0)
        ax.set_ylim(-0.4, 1.0)
        ax.axis('off')
        ax.set_aspect('equal')
        
        self.canvas.draw()
        
        status = "PAGE FAULT" if page_fault else "HIT"
        status_color = "red" if page_fault else "green"
        tlb_status = f" | TLB: {'HIT' if tlb_hit else 'MISS'}" if tlb_hit is not None else ""
        
        self.info_label.setText(
            f"<b>Step {step_data['step']}</b>: "
            f"Accessing page <b>{page}</b> → "
            f"<span style='color: {status_color}; font-weight: bold;'>{status}</span>"
            f"{tlb_status}"
        )
        
        self.step_label.setText(f"Step: {self.current_step + 1}/{len(self.history)}")
