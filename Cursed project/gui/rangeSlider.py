from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor


class RangeSlider(QWidget):
    valueChanged = pyqtSignal(int, int)

    def __init__(self, minimum=0, maximum=100, lowerValue=50, upperValue=80, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(30)

        self._min = minimum
        self._max = maximum
        self._lower = lowerValue
        self._upper = upperValue

        self._moving = None

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()

        # Background line
        painter.setBrush(QBrush(QColor(180, 180, 180)))
        painter.drawRect(0, h // 2 - 3, w, 6)

        # Selected range
        left = int((self._lower - self._min) / (self._max - self._min) * w)
        right = int((self._upper - self._min) / (self._max - self._min) * w)

        painter.setBrush(QBrush(QColor(70, 130, 180)))
        painter.drawRect(left, h // 2 - 3, right - left, 6)

        # Handles
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawEllipse(QRect(left - 7, h // 2 - 7, 14, 14))
        painter.drawEllipse(QRect(right - 7, h // 2 - 7, 14, 14))

    def mousePressEvent(self, event):
        w = self.width()
        e_x = event.x()

        lower_x = int((self._lower - self._min) / (self._max - self._min) * w)
        upper_x = int((self._upper - self._min) / (self._max - self._min) * w)

        if abs(e_x - lower_x) < 10:
            self._moving = 'lower'
        elif abs(e_x - upper_x) < 10:
            self._moving = 'upper'

    def mouseMoveEvent(self, event):
        if not self._moving:
            return

        w = self.width()
        value = (event.x() / w) * (self._max - self._min) + self._min
        value = max(self._min, min(self._max, int(value)))

        if self._moving == 'lower':
            if value < self._upper:
                self._lower = value
        else:
            if value > self._lower:
                self._upper = value

        self.valueChanged.emit(self._lower, self._upper)
        self.update()

    def mouseReleaseEvent(self, event):
        self._moving = None

    def setValue(self, lower, upper):
        self._lower = lower
        self._upper = upper
        self.update()

    def values(self):
        return self._lower, self._upper