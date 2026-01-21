"""
Custom animated widgets for Virtual Memory Simulator
Provides smooth, fluid animations and transitions
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QGraphicsOpacityEffect, QFrame, QPushButton)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QTimer, 
                          QParallelAnimationGroup, QSequentialAnimationGroup,
                          pyqtProperty, QPoint, QSize, QRect)
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen, QBrush, QPainterPath, QFont
import math


class AnimatedCard(QFrame):
    """A card widget with smooth hover animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_offset = 0
        self._glow_opacity = 0
        
        self.setObjectName("animatedCard")
        self.setup_animations()
        
    def setup_animations(self):
        # Hover animation for lift effect
        self._lift_anim = QPropertyAnimation(self, b"hover_offset")
        self._lift_anim.setDuration(200)
        self._lift_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Glow animation
        self._glow_anim = QPropertyAnimation(self, b"glow_opacity")
        self._glow_anim.setDuration(200)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    @pyqtProperty(int)
    def hover_offset(self):
        return self._hover_offset
    
    @hover_offset.setter
    def hover_offset(self, value):
        self._hover_offset = value
        self.update()
        
    @pyqtProperty(float)
    def glow_opacity(self):
        return self._glow_opacity
    
    @glow_opacity.setter
    def glow_opacity(self, value):
        self._glow_opacity = value
        self.update()
        
    def enterEvent(self, event):
        self._lift_anim.setStartValue(self._hover_offset)
        self._lift_anim.setEndValue(-4)
        self._lift_anim.start()
        
        self._glow_anim.setStartValue(self._glow_opacity)
        self._glow_anim.setEndValue(0.3)
        self._glow_anim.start()
        
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._lift_anim.setStartValue(self._hover_offset)
        self._lift_anim.setEndValue(0)
        self._lift_anim.start()
        
        self._glow_anim.setStartValue(self._glow_opacity)
        self._glow_anim.setEndValue(0)
        self._glow_anim.start()
        
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(4, 4 + self._hover_offset, -4, -4 + self._hover_offset)
        
        # Draw shadow
        shadow_rect = rect.adjusted(2, 2, 2, 2)
        shadow_color = QColor(0, 0, 0, 60)
        painter.setBrush(shadow_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(shadow_rect, 12, 12)
        
        # Draw glow if hovering
        if self._glow_opacity > 0:
            glow_color = QColor(14, 165, 168, int(255 * self._glow_opacity))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(glow_color, 2))
            painter.drawRoundedRect(rect.adjusted(-2, -2, 2, 2), 14, 14)
        
        # Draw card background
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QColor(31, 41, 55))
        gradient.setColorAt(1, QColor(17, 24, 39))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(71, 85, 105), 1))
        painter.drawRoundedRect(rect, 12, 12)
        
        painter.end()


class PulsingDot(QWidget):
    """Animated pulsing indicator dot"""
    
    def __init__(self, color="#10b981", size=12, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._size = size
        self._pulse_scale = 1.0
        self._pulse_opacity = 1.0
        
        self.setFixedSize(size * 3, size * 3)
        self.setup_animation()
        
    def setup_animation(self):
        self._scale_anim = QPropertyAnimation(self, b"pulse_scale")
        self._scale_anim.setDuration(1500)
        self._scale_anim.setStartValue(1.0)
        self._scale_anim.setEndValue(2.0)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._scale_anim.setLoopCount(-1)  # Infinite loop
        
        self._opacity_anim = QPropertyAnimation(self, b"pulse_opacity")
        self._opacity_anim.setDuration(1500)
        self._opacity_anim.setStartValue(0.6)
        self._opacity_anim.setEndValue(0.0)
        self._opacity_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._opacity_anim.setLoopCount(-1)
        
    def start(self):
        self._scale_anim.start()
        self._opacity_anim.start()
        
    def stop(self):
        self._scale_anim.stop()
        self._opacity_anim.stop()
        
    @pyqtProperty(float)
    def pulse_scale(self):
        return self._pulse_scale
    
    @pulse_scale.setter
    def pulse_scale(self, value):
        self._pulse_scale = value
        self.update()
        
    @pyqtProperty(float)
    def pulse_opacity(self):
        return self._pulse_opacity
    
    @pulse_opacity.setter
    def pulse_opacity(self, value):
        self._pulse_opacity = value
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        
        # Draw pulsing ring
        ring_color = QColor(self._color)
        ring_color.setAlphaF(self._pulse_opacity)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(ring_color, 2))
        radius = (self._size / 2) * self._pulse_scale
        painter.drawEllipse(center, int(radius), int(radius))
        
        # Draw solid center dot
        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, self._size // 2, self._size // 2)
        
        painter.end()


class AnimatedProgressRing(QWidget):
    """Circular progress indicator with smooth animation"""
    
    def __init__(self, size=80, thickness=8, parent=None):
        super().__init__(parent)
        self._size = size
        self._thickness = thickness
        self._progress = 0
        self._target_progress = 0
        self._rotation = 0
        
        self.setFixedSize(size, size)
        self.setup_animations()
        
    def setup_animations(self):
        self._progress_anim = QPropertyAnimation(self, b"progress")
        self._progress_anim.setDuration(800)
        self._progress_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Continuous rotation for indeterminate state
        self._rotation_anim = QPropertyAnimation(self, b"rotation")
        self._rotation_anim.setDuration(1200)
        self._rotation_anim.setStartValue(0)
        self._rotation_anim.setEndValue(360)
        self._rotation_anim.setLoopCount(-1)
        
    @pyqtProperty(float)
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        self._progress = value
        self.update()
        
    @pyqtProperty(int)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.update()
        
    def set_progress(self, value):
        """Animate to a new progress value (0-100)"""
        self._target_progress = max(0, min(100, value))
        self._progress_anim.setStartValue(self._progress)
        self._progress_anim.setEndValue(self._target_progress)
        self._progress_anim.start()
        
    def set_indeterminate(self, indeterminate=True):
        """Toggle indeterminate spinning mode"""
        if indeterminate:
            self._rotation_anim.start()
        else:
            self._rotation_anim.stop()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(
            self._thickness, self._thickness,
            -self._thickness, -self._thickness
        )
        
        # Draw background ring
        painter.setPen(QPen(QColor(51, 65, 85), self._thickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(rect)
        
        # Draw progress arc
        if self._progress > 0:
            gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
            gradient.setColorAt(0, QColor(14, 165, 168))
            gradient.setColorAt(1, QColor(245, 158, 11))
            
            pen = QPen(QBrush(gradient), self._thickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-self._progress * 3.6 * 16)  # Qt uses 1/16th of a degree
            start_angle = (90 + self._rotation) * 16
            painter.drawArc(rect, start_angle, span_angle)
        
        painter.end()


class AnimatedCounter(QLabel):
    """Label that animates number changes"""
    
    def __init__(self, prefix="", suffix="", decimals=0, parent=None):
        super().__init__(parent)
        self._value = 0
        self._display_value = 0.0
        self._prefix = prefix
        self._suffix = suffix
        self._decimals = decimals
        
        self.setup_animation()
        self.update_text()
        
    def setup_animation(self):
        self._anim = QPropertyAnimation(self, b"display_value")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.valueChanged.connect(self.update_text)
        
    @pyqtProperty(float)
    def display_value(self):
        return self._display_value
    
    @display_value.setter
    def display_value(self, value):
        self._display_value = value
        
    def set_value(self, value):
        """Animate to a new value"""
        self._anim.setStartValue(self._display_value)
        self._anim.setEndValue(float(value))
        self._anim.start()
        self._value = value
        
    def update_text(self):
        if self._decimals == 0:
            text = f"{self._prefix}{int(self._display_value)}{self._suffix}"
        else:
            text = f"{self._prefix}{self._display_value:.{self._decimals}f}{self._suffix}"
        self.setText(text)


class GlowButton(QPushButton):
    """Button with animated glow effect"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._glow_radius = 0
        self._glow_color = QColor(14, 165, 168, 100)
        
        self.setup_animation()
        
    def setup_animation(self):
        self._glow_anim = QPropertyAnimation(self, b"glow_radius")
        self._glow_anim.setDuration(200)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    @pyqtProperty(int)
    def glow_radius(self):
        return self._glow_radius
    
    @glow_radius.setter
    def glow_radius(self, value):
        self._glow_radius = value
        self.update()
        
    def enterEvent(self, event):
        self._glow_anim.setStartValue(self._glow_radius)
        self._glow_anim.setEndValue(15)
        self._glow_anim.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._glow_anim.setStartValue(self._glow_radius)
        self._glow_anim.setEndValue(0)
        self._glow_anim.start()
        super().leaveEvent(event)


class WaveWidget(QWidget):
    """Animated wave background widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._phase = 0
        self._wave_colors = [
            QColor(14, 165, 168, 30),
            QColor(245, 158, 11, 20),
            QColor(56, 189, 248, 25),
        ]
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.animate)
        self._timer.start(50)  # 20 FPS
        
    def animate(self):
        self._phase += 0.1
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        for i, color in enumerate(self._wave_colors):
            path = QPainterPath()
            path.moveTo(0, height)
            
            amplitude = 15 + i * 5
            frequency = 0.02 - i * 0.005
            phase_offset = self._phase + i * 1.5
            y_offset = height - 50 - i * 30
            
            for x in range(0, width + 10, 10):
                y = y_offset + amplitude * math.sin(frequency * x + phase_offset)
                if x == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
                    
            path.lineTo(width, height)
            path.lineTo(0, height)
            path.closeSubpath()
            
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(path)
            
        painter.end()


class FadeWidget(QWidget):
    """Widget with fade in/out capabilities"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        
        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_anim.setDuration(300)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
    def fade_in(self, duration=300):
        self._fade_anim.setDuration(duration)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self.show()
        self._fade_anim.start()
        
    def fade_out(self, duration=300):
        self._fade_anim.setDuration(duration)
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.finished.connect(self.hide)
        self._fade_anim.start()


class SlideWidget(QWidget):
    """Widget with slide in/out animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._slide_anim = QPropertyAnimation(self, b"pos")
        self._slide_anim.setDuration(400)
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def slide_in_from_right(self):
        start_pos = QPoint(self.parent().width() if self.parent() else 800, self.y())
        end_pos = QPoint(self.x(), self.y())
        
        self._slide_anim.setStartValue(start_pos)
        self._slide_anim.setEndValue(end_pos)
        self.show()
        self._slide_anim.start()
        
    def slide_in_from_bottom(self):
        start_pos = QPoint(self.x(), self.parent().height() if self.parent() else 600)
        end_pos = QPoint(self.x(), self.y())
        
        self._slide_anim.setStartValue(start_pos)
        self._slide_anim.setEndValue(end_pos)
        self.show()
        self._slide_anim.start()


class StatsCard(QFrame):
    """Modern stats display card with icon and animated value"""
    
    def __init__(self, title="", icon="", color="primary", parent=None):
        super().__init__(parent)
        self._title = title
        self._icon = icon
        self._color = color
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Header with icon
        header = QHBoxLayout()
        
        if self._icon:
            icon_label = QLabel(self._icon)
            icon_label.setStyleSheet("font-size: 24px;")
            header.addWidget(icon_label)
            
        title_label = QLabel(self._title)
        title_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8); font-weight: 500;")
        header.addWidget(title_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Animated value
        self.value_label = AnimatedCounter()
        self.value_label.setStyleSheet("font-size: 28px; font-weight: 700; color: white;")
        layout.addWidget(self.value_label)
        
        # Subtitle
        self.subtitle_label = QLabel()
        self.subtitle_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.7);")
        layout.addWidget(self.subtitle_label)
        
        # Apply color theme
        self.apply_color_theme()
        
    def apply_color_theme(self):
        colors = {
            'primary': ('14, 165, 168', '15, 118, 110'),
            'success': ('34, 197, 94', '22, 163, 74'),
            'warning': ('249, 115, 22', '234, 88, 12'),
            'error': ('239, 68, 68', '220, 38, 38'),
            'accent': ('56, 189, 248', '2, 132, 199'),
            'secondary': ('245, 158, 11', '217, 119, 6'),
        }
        
        c = colors.get(self._color, colors['primary'])
        self.setStyleSheet(f"""
            StatsCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb({c[0]}), stop:1 rgb({c[1]}));
                border: none;
                border-radius: 12px;
            }}
        """)
        
    def set_value(self, value, subtitle=""):
        self.value_label.set_value(value)
        if subtitle:
            self.subtitle_label.setText(subtitle)
