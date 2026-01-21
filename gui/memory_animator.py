"""
Enhanced Memory Animator with fluid animations
Beautiful step-by-step visualization of page replacement
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QFrame, QGraphicsDropShadowEffect,
                             QSizePolicy)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, 
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          pyqtProperty, QPoint, QRectF, QPointF)
from PyQt6.QtGui import (QPainter, QColor, QLinearGradient, QPen, QBrush, 
                         QPainterPath, QFont, QRadialGradient)
import math

from gui.styles import COLORS


class MemoryFrameWidget(QWidget):
    """Individual memory frame with animations"""
    
    def __init__(self, frame_index, parent=None):
        super().__init__(parent)
        self.frame_index = frame_index
        self._page = None
        self._prev_page = None
        self._is_highlighted = False
        self._highlight_intensity = 0.0
        self._scale = 1.0
        self._glow_radius = 0
        self._is_new_page = False
        
        self.setFixedSize(110, 140)
        self.setup_animations()
        
    def setup_animations(self):
        self._highlight_anim = QPropertyAnimation(self, b"highlight_intensity")
        self._highlight_anim.setDuration(400)
        self._highlight_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(300)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        self._glow_anim = QPropertyAnimation(self, b"glow_radius")
        self._glow_anim.setDuration(500)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    @pyqtProperty(float)
    def highlight_intensity(self):
        return self._highlight_intensity
    
    @highlight_intensity.setter
    def highlight_intensity(self, value):
        self._highlight_intensity = value
        self.update()
        
    @pyqtProperty(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()
        
    @pyqtProperty(int)
    def glow_radius(self):
        return self._glow_radius
    
    @glow_radius.setter
    def glow_radius(self, value):
        self._glow_radius = value
        self.update()
        
    def set_page(self, page, is_current=False):
        """Set the page number with animation"""
        old_page = self._page
        self._page = page
        self._is_new_page = (page is not None and page != old_page)
        
        if self._is_new_page:
            # Pop animation when new page arrives
            self._scale_anim.setStartValue(0.7)
            self._scale_anim.setEndValue(1.0)
            self._scale_anim.start()
            
        if is_current:
            self.highlight(True)
        else:
            self.highlight(False)
            
        self.update()
        
    def highlight(self, enable):
        """Enable/disable highlight animation"""
        self._is_highlighted = enable
        self._highlight_anim.setStartValue(self._highlight_intensity)
        self._highlight_anim.setEndValue(1.0 if enable else 0.0)
        self._highlight_anim.start()
        
        self._glow_anim.setStartValue(self._glow_radius)
        self._glow_anim.setEndValue(15 if enable else 0)
        self._glow_anim.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate scaled dimensions with padding for glow/label
        width = int(75 * self._scale)
        height = int(90 * self._scale)
        x = (self.width() - width) // 2
        y = (self.height() - height) // 2 - 5
        
        rect = QRectF(x, y, width, height)
        
        # Draw glow effect
        if self._glow_radius > 0:
            glow_color = QColor(14, 165, 168, int(100 * self._highlight_intensity))
            for i in range(self._glow_radius, 0, -3):
                glow_color.setAlpha(int(30 * (1 - i / self._glow_radius)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(glow_color)
                painter.drawRoundedRect(rect.adjusted(-i, -i, i, i), 14, 14)
        
        # Draw frame background
        if self._page is not None:
            # Gradient based on highlight and new page status
            gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
            if self._highlight_intensity > 0:
                # Highlighted (current page being accessed)
                gradient.setColorAt(0, QColor(14, 165, 168, int(255 * self._highlight_intensity) + 100))
                gradient.setColorAt(1, QColor(15, 118, 110, int(200 * self._highlight_intensity) + 80))
            else:
                # Normal filled frame
                gradient.setColorAt(0, QColor(51, 65, 85))
                gradient.setColorAt(1, QColor(30, 41, 59))
            painter.setBrush(gradient)
        else:
            # Empty frame
            painter.setBrush(QColor(30, 41, 59, 150))
            
        # Border - highlight with green for new, purple for current, gray for normal
        if self._is_new_page and self._highlight_intensity > 0.5:
            border_color = QColor(16, 185, 129)  # Green for newly loaded
            border_width = 3
        elif self._highlight_intensity > 0.5:
            border_color = QColor(14, 165, 168)  # Teal for current access
            border_width = 2
        else:
            border_color = QColor(71, 85, 105)
            border_width = 1
            
        painter.setPen(QPen(border_color, border_width))
        painter.drawRoundedRect(rect, 12, 12)
        
        # Draw page number or empty indicator
        if self._page is not None:
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Page number
            font = QFont("Helvetica Neue", 22, QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self._page))
        else:
            # Empty indicator
            painter.setPen(QPen(QColor(100, 116, 139), 2, Qt.PenStyle.DashLine))
            inner_rect = rect.adjusted(15, 25, -15, -25)
            painter.drawRoundedRect(inner_rect, 6, 6)
            
            font = QFont("Helvetica Neue", 9)
            painter.setFont(font)
            painter.setPen(QColor(100, 116, 139))
            painter.drawText(rect.adjusted(0, 15, 0, 0), Qt.AlignmentFlag.AlignCenter, "Empty")
        
        # Frame label
        font = QFont("Helvetica Neue", 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(148, 163, 184))
        label_rect = QRectF(x, y + height + 5, width, 20)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, f"Frame {self.frame_index}")
        
        painter.end()


class IncomingPageWidget(QWidget):
    """Animated incoming page indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._page = None
        self._is_fault = False
        self._pulse_phase = 0.0
        self._entry_progress = 0.0
        
        self.setFixedSize(140, 150)
        
        # Pulse animation
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._update_pulse)
        self._pulse_timer.start(50)
        
        self.setup_animations()
        
    def setup_animations(self):
        self._entry_anim = QPropertyAnimation(self, b"entry_progress")
        self._entry_anim.setDuration(400)
        self._entry_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
    @pyqtProperty(float)
    def entry_progress(self):
        return self._entry_progress
    
    @entry_progress.setter
    def entry_progress(self, value):
        self._entry_progress = value
        self.update()
        
    def _update_pulse(self):
        self._pulse_phase += 0.15
        if self._pulse_phase > 2 * math.pi:
            self._pulse_phase = 0
        self.update()
        
    def set_page(self, page, is_fault=False):
        """Set the incoming page with entry animation"""
        self._page = page
        self._is_fault = is_fault
        
        self._entry_anim.setStartValue(0.0)
        self._entry_anim.setEndValue(1.0)
        self._entry_anim.start()
        
        self.update()
        
    def paintEvent(self, event):
        if self._page is None:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2 - 12)
        max_radius = min(self.width(), self.height()) / 2 - 14
        max_ring_padding = 31
        base_radius = max(0.0, (max_radius - max_ring_padding) * self._entry_progress)
        
        # Pulsing outer rings
        pulse_offset = (math.sin(self._pulse_phase) + 1) / 2
        
        for i in range(3):
            ring_radius = base_radius + 10 + i * 8 + pulse_offset * 5
            alpha = int(80 - i * 25)
            if self._is_fault:
                ring_color = QColor(239, 68, 68, alpha)
            else:
                ring_color = QColor(16, 185, 129, alpha)
                
            painter.setPen(QPen(ring_color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(center, ring_radius, ring_radius)
        
        # Main circle with gradient
        gradient = QRadialGradient(center, base_radius)
        if self._is_fault:
            gradient.setColorAt(0, QColor(248, 113, 113))
            gradient.setColorAt(1, QColor(220, 38, 38))
        else:
            gradient.setColorAt(0, QColor(52, 211, 153))
            gradient.setColorAt(1, QColor(5, 150, 105))
            
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        painter.drawEllipse(center, base_radius, base_radius)
        
        # Page number
        font = QFont("Helvetica Neue", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        text_rect = QRectF(center.x() - 25, center.y() - 15, 50, 30)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(self._page))
        
        # Status label
        font = QFont("Helvetica Neue", 10, QFont.Weight.Bold)
        painter.setFont(font)
        status_text = "FAULT" if self._is_fault else "HIT"
        status_color = QColor(254, 202, 202) if self._is_fault else QColor(167, 243, 208)
        painter.setPen(status_color)
        status_rect = QRectF(0, self.height() - 30, self.width(), 20)
        painter.drawText(status_rect, Qt.AlignmentFlag.AlignCenter, status_text)
        
        # Arrow pointing to frames
        if self._entry_progress > 0.5:
            arrow_alpha = int(255 * (self._entry_progress - 0.5) * 2)
            arrow_color = QColor(148, 163, 184, arrow_alpha)
            painter.setPen(QPen(arrow_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            
            start_x = 18
            end_x = 4
            y = center.y()
            
            painter.drawLine(QPointF(start_x, y), QPointF(end_x, y))
            
            # Arrowhead
            painter.drawLine(QPointF(end_x, y), QPointF(end_x + 8, y - 6))
            painter.drawLine(QPointF(end_x, y), QPointF(end_x + 8, y + 6))
        
        painter.end()


class MemoryAnimator(QWidget):
    """Enhanced Memory Frame Animation with fluid transitions"""
    
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_step = 0
        self.is_playing = False
        self.frame_widgets = []
        self.num_frames = 3
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_frame = QFrame()
        title_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(14, 165, 168, 0.2), stop:1 rgba(245, 158, 11, 0.2));
                border-radius: 12px;
                padding: 8px;
            }}
        """)
        title_layout = QHBoxLayout(title_frame)
        
        title = QLabel("🎬 Memory Frame Animation")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        self.step_badge = QLabel("Step 0/0")
        self.step_badge.setStyleSheet(f"""
            background-color: {COLORS['primary']};
            color: white;
            padding: 6px 14px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
        """)
        title_layout.addWidget(self.step_badge)
        
        layout.addWidget(title_frame)
        
        # Animation canvas area
        self.canvas_frame = QFrame()
        self.canvas_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_medium']};
                border: 1px solid {COLORS['border']};
                border-radius: 16px;
            }}
        """)
        self.canvas_frame.setMinimumHeight(240)
        
        canvas_layout = QHBoxLayout(self.canvas_frame)
        canvas_layout.setContentsMargins(30, 30, 30, 30)
        canvas_layout.setSpacing(15)
        
        # Memory frames container
        self.frames_container = QWidget()
        self.frames_layout = QHBoxLayout(self.frames_container)
        self.frames_layout.setSpacing(10)
        canvas_layout.addWidget(self.frames_container)
        
        canvas_layout.addStretch()
        
        # Incoming page widget
        self.incoming_widget = IncomingPageWidget()
        canvas_layout.addWidget(self.incoming_widget)
        
        layout.addWidget(self.canvas_frame)
        
        # Info panel
        self.info_panel = QFrame()
        self.info_panel.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(14, 165, 168, 0.1);
                border: 1px solid {COLORS['primary']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        info_layout = QHBoxLayout(self.info_panel)
        
        self.info_icon = QLabel("ℹ️")
        self.info_icon.setStyleSheet("font-size: 20px;")
        info_layout.addWidget(self.info_icon)
        
        self.info_label = QLabel("Load a simulation to begin animation")
        self.info_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        """)
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label, 1)
        
        layout.addWidget(self.info_panel)
        
        # Controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_light']};
                border-radius: 12px;
                padding: 8px;
            }}
        """)
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(12)
        
        # Playback buttons
        self.play_button = self.create_control_button("▶️", "Play")
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)
        
        self.step_button = self.create_control_button("⏭️", "Next")
        self.step_button.clicked.connect(self.next_step)
        controls_layout.addWidget(self.step_button)
        
        self.prev_button = self.create_control_button("⏮️", "Prev")
        self.prev_button.clicked.connect(self.prev_step)
        controls_layout.addWidget(self.prev_button)
        
        self.reset_button = self.create_control_button("🔄", "Reset")
        self.reset_button.clicked.connect(self.reset)
        controls_layout.addWidget(self.reset_button)
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {COLORS['bg_medium']};
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
                border: 2px solid white;
            }}
            QSlider::sub-page:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
                border-radius: 4px;
            }}
        """)
        controls_layout.addWidget(self.slider, 1)
        
        # Speed control
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-weight: 500;")
        controls_layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.speed_slider.setFixedWidth(100)
        self.speed_slider.valueChanged.connect(self.update_speed)
        controls_layout.addWidget(self.speed_slider)
        
        layout.addWidget(controls_frame)
        
        # Timer for playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.playback_speed = 800
        
    def create_control_button(self, icon, tooltip):
        """Create a styled control button"""
        btn = QPushButton(icon)
        btn.setToolTip(tooltip)
        btn.setFixedSize(50, 50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_medium']};
                border: 2px solid {COLORS['border']};
                border-radius: 12px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
            }}
        """)
        return btn
        
    def load_results(self, results):
        """Load simulation results for animation"""
        self.history = results.get('history', [])
        self.num_frames = results.get('num_frames', self.num_frames)
        self.current_step = 0
        self.slider.setMaximum(len(self.history) - 1 if self.history else 0)
        self.slider.setValue(0)
        
        # Create frame widgets
        self.create_frame_widgets()
        self.update_display()
        
    def create_frame_widgets(self):
        """Create memory frame widgets based on results"""
        # Clear existing
        for widget in self.frame_widgets:
            widget.deleteLater()
        self.frame_widgets.clear()
        
        # Determine number of frames
        num_frames = self.num_frames
        if num_frames <= 0 and self.history:
            num_frames = len(self.history[0].get('frames', []))
        if num_frames <= 0:
            num_frames = 3
            
        # Create new frame widgets
        for i in range(num_frames):
            frame_widget = MemoryFrameWidget(i)
            self.frames_layout.addWidget(frame_widget)
            self.frame_widgets.append(frame_widget)
            
    def update_speed(self, value):
        """Update playback speed"""
        self.playback_speed = 1500 - (value * 120)
        if self.is_playing:
            self.timer.setInterval(self.playback_speed)
        
    def toggle_play(self):
        """Toggle animation playback"""
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText("▶️")
            self.is_playing = False
        else:
            self.timer.start(self.playback_speed)
            self.play_button.setText("⏸️")
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
                
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.slider.setValue(self.current_step)
            self.update_display()
                
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
        """Update the visual display with animations"""
        if not self.history or self.current_step >= len(self.history):
            return
            
        step_data = self.history[self.current_step]
        frames = step_data.get('frames', [])
        page = step_data.get('page')
        page_fault = step_data.get('page_fault', False)
        tlb_hit = step_data.get('tlb_hit')
        
        # Get previous frames to detect changes
        prev_frames = []
        if self.current_step > 0:
            prev_frames = self.history[self.current_step - 1].get('frames', [])
        
        # Update frame widgets
        for i, frame_widget in enumerate(self.frame_widgets):
            if i < len(frames):
                current_page = frames[i]
                prev_page = prev_frames[i] if i < len(prev_frames) else None
                
                # Check if this frame was just modified (new page loaded here)
                is_modified = (current_page != prev_page) and (current_page == page)
                # Check if this is where the current page resides
                is_current = (current_page == page)
                
                frame_widget.set_page(current_page, is_current and (page_fault or is_modified))
            else:
                frame_widget.set_page(None, False)
                
        # Update incoming page widget
        self.incoming_widget.set_page(page, page_fault)
        
        # Update info panel
        status_icon = "❌" if page_fault else "✅"
        status_text = "PAGE FAULT - Page loaded into memory" if page_fault else "HIT - Page found in memory"
        status_color = COLORS['error'] if page_fault else COLORS['success']
        
        # Find which frame contains the page
        frame_info = ""
        if page in frames:
            frame_idx = frames.index(page)
            frame_info = f" (Frame {frame_idx})"
        
        tlb_info = ""
        if tlb_hit is not None:
            tlb_icon = "⚡" if tlb_hit else "○"
            tlb_text = "TLB HIT" if tlb_hit else "TLB MISS"
            tlb_info = f" • {tlb_icon} {tlb_text}"
        
        self.info_icon.setText(status_icon)
        self.info_label.setText(
            f"<b>Step {step_data['step']}</b>: Accessing page <b>{page}</b>{frame_info} → "
            f"<span style='color: {status_color};'><b>{status_text}</b></span>{tlb_info}"
        )
        
        self.info_panel.setStyleSheet(f"""
            QFrame {{
                background-color: rgba({'239, 68, 68' if page_fault else '34, 197, 94'}, 0.1);
                border: 1px solid {status_color};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        
        # Update step badge
        self.step_badge.setText(f"Step {self.current_step + 1}/{len(self.history)}")
