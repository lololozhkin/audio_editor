from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygon
from PyQt5.QtCore import Qt, QRect, QLine, QPoint
import sys
import math


class TwoPointersSlider(QWidget):
    mainPosChanged = QtCore.pyqtSignal(int)
    leftPosChanged = QtCore.pyqtSignal(int)
    rightPosChanged = QtCore.pyqtSignal(int)
    endOfRange = QtCore.pyqtSignal()
    mainSliderMoved = QtCore.pyqtSignal(int)

    @property
    def main_pointer_pos(self):
        return self._main_pointer_pos

    @property
    def main_pointer_pos_x(self):
        return self.from_max_to_x(self._main_pointer_pos)

    @main_pointer_pos.setter
    def main_pointer_pos(self, position):
        self._main_pointer_pos = position

    @property
    def first_pointer_pos(self):
        return self._first_pointer_pos

    @property
    def first_pointer_pos_x(self):
        return self.from_max_to_x(self._first_pointer_pos)

    @first_pointer_pos.setter
    def first_pointer_pos(self, position):
        self._first_pointer_pos = position

    @property
    def second_pointer_pos(self):
        return self._second_pointer_pos

    @property
    def second_pointer_pos_x(self):
        return self.from_max_to_x(self._second_pointer_pos)

    @second_pointer_pos.setter
    def second_pointer_pos(self, position):
        self._second_pointer_pos = position

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        self.first_pointer_pos = 0
        self.second_pointer_pos = 100
        self.main_pointer_pos = 0
        self.maximum = 100

        self.mainPosChanged.connect(lambda x: self.update())
        # self.mainPosChanged.connect(lambda x: self.end_of_range_check())

        self.rightPosChanged.connect(lambda x: self.update())
        # self.rightPosChanged.connect(lambda x: self.end_of_range_check())

        self.leftPosChanged.connect(lambda x: self.update())

        self.first_taken = False
        self.second_taken = False
        self.main_taken = False

    def init_ui(self):
        # self.setMinimumHeight(20)
        # self.setMinimumWidth(50)

        self.left_padding = 20
        self.right_padding = 20

        self.pointer_radius = 8
        self.line_width = 10
        self.line_pos_fraq = 1 / 2

        self.main_pointer_height = 15
        self.main_pointer_width = 9

        self.selected_range_color = QColor(250, 169, 167)
        self.main_line_color = QColor(82, 82, 82)
        self.pointers_color = QColor(214, 209, 209)

    def set_maximum(self, val):
        if val < 0:
            raise ValueError
        self.maximum = val
        self.first_pointer_pos = 0
        self.second_pointer_pos = self.maximum
        self.main_pointer_pos = 0

    def paintEvent(self, e: QtGui.QPaintEvent):
        painter = QPainter(self)

        self.draw_widget(painter)

    def draw_widget(self, painter: QPainter):
        size = self.size()
        w = size.width()
        h = self.height()
        line_pos = h * self.line_pos_fraq

        pen = QPen()
        brush = QBrush()
        pen.setColor(self.main_line_color)
        pen.setWidth(self.line_width)
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.drawLine(QLine(self.left_padding,
                               line_pos,
                               w - self.right_padding,
                               line_pos))

        # 161, 255, 236
        pen.setColor(self.selected_range_color)
        painter.setPen(pen)
        painter.drawLine(QLine(self.first_pointer_pos_x, line_pos,
                               self.second_pointer_pos_x, line_pos))

        pen.setWidth(1)
        pen.setColor(QColor(0, 0, 0))
        brush.setColor(self.pointers_color)
        brush.setStyle(Qt.SolidPattern)

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.circle_rect(self.first_pointer_pos_x,
                                             line_pos,
                                             self.pointer_radius))
        painter.drawEllipse(self.circle_rect(self.second_pointer_pos_x,
                                             line_pos,
                                             self.pointer_radius))

        painter.drawPolygon(QPolygon(self.draw_main_pointer()))

    @staticmethod
    def circle_rect(centre_x, centre_y, radius):
        return QRect(centre_x - radius,
                     centre_y - radius,
                     2 * radius, 2 * radius)

    def draw_main_pointer(self):
        points = []
        line_pos = self.height() * self.line_pos_fraq
        fraq = 2 / 3
        points.append(QPoint(self.main_pointer_pos_x +
                             self.main_pointer_width / 2,

                             line_pos - self.line_width / 2 -
                             self.main_pointer_height))

        points.append(QPoint(self.main_pointer_pos_x -
                             self.main_pointer_width / 2,

                             line_pos - self.line_width / 2 -
                             self.main_pointer_height))

        points.append(QPoint(self.main_pointer_pos_x -
                             self.main_pointer_width / 2,

                             line_pos - self.line_width / 2 -
                             (1 - fraq) * self.main_pointer_height))

        points.append(QPoint(self.main_pointer_pos_x,
                             line_pos - self.line_width / 2))

        points.append(QPoint(self.main_pointer_pos_x +
                             self.main_pointer_width / 2,

                             line_pos - self.line_width / 2 -
                             (1 - fraq) * self.main_pointer_height))
        return points

    def set_main_pos(self, new_pos):
        old_pos = self.main_pointer_pos
        self.main_pointer_pos = max(self.first_pointer_pos,
                                    new_pos)
        if self.main_pointer_pos > self.second_pointer_pos:
            self.main_pointer_pos = self.second_pointer_pos
            self.endOfRange.emit()

        if old_pos != self.main_pointer_pos:
            self.mainPosChanged.emit(self.main_pointer_pos)

    def set_left_pos(self, new_pos):
        old_pos = self.first_pointer_pos
        self.first_pointer_pos = min(new_pos, self.second_pointer_pos)
        self.first_pointer_pos = max(0, self.first_pointer_pos)
        if self.main_pointer_pos < self.first_pointer_pos:
            self.set_main_pos(self.first_pointer_pos)
            self.mainSliderMoved.emit(self.main_pointer_pos)

        if old_pos != self.first_pointer_pos:
            self.leftPosChanged.emit(self.first_pointer_pos)

    def set_right_pos(self, new_pos):
        old_pos = self.second_pointer_pos
        self.second_pointer_pos = max(new_pos, self.first_pointer_pos)
        self.second_pointer_pos = min(self.maximum, self.second_pointer_pos)

        if self.main_pointer_pos > self.second_pointer_pos:
            self.set_main_pos(self.second_pointer_pos)
            self.mainSliderMoved.emit(self.main_pointer_pos)
            self.endOfRange.emit()

        if old_pos != self.second_pointer_pos:
            self.rightPosChanged.emit(self.second_pointer_pos)

    def get_distance(self, first_point, second_point):
        return math.sqrt((first_point.x() - second_point.x()) ** 2 +
                         (first_point.y() - second_point.y()) ** 2)

    def mousePressEvent(self, e):
        pos = e.pos()
        if QPolygon(self.draw_main_pointer()).containsPoint(pos,
                                                            Qt.OddEvenFill):
            self.main_taken = True
            return

        line_pos = self.height() * self.line_pos_fraq
        if self.get_distance(pos, QPoint(self.first_pointer_pos_x, line_pos)) \
                <= self.pointer_radius:

            self.first_taken = True

        if self.get_distance(pos, QPoint(self.second_pointer_pos_x, line_pos))\
                <= self.pointer_radius:

            self.second_taken = True

        if self.first_taken and self.second_taken:
            if self.first_pointer_pos > 0:
                self.second_taken = False
            else:
                self.first_taken = False

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if self.first_taken:
            self.set_left_pos(self.from_x_to_max(e.pos().x()))
        if self.second_taken:
            self.set_right_pos(self.from_x_to_max(e.pos().x()))
        if self.main_taken:
            self.set_main_pos(self.from_x_to_max(e.pos().x()))
            self.mainSliderMoved.emit(self.main_pointer_pos)

    def mouseReleaseEvent(self, e):
        self.first_taken = self.second_taken = self.main_taken = False

    def end_of_range_check(self):
        return self.main_pointer_pos >= self.second_pointer_pos

    def from_max_to_x(self, check_pos):
        breadth = self.width() - self.left_padding - self.right_padding
        fraq = check_pos / self.maximum
        pos = self.left_padding + breadth * fraq
        return pos

    def from_x_to_max(self, pos):
        breadth = self.width() - self.left_padding - self.right_padding
        pos_on_line = pos - self.left_padding
        return (pos_on_line / breadth) * self.maximum


def main():
    app = QApplication(sys.argv)
    ex = TwoPointersSlider()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
