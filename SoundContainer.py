from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPainter, QPen, QColor, QDrag
from PyQt5.QtCore import QUrl, QRect, QSize, QPoint, QLine, QMimeData

from Fragment import Fragment
from FragmentMimeData import FragmentMimeData
import os


BTN_STYLE = \
    """
QPushButton
{
    color: #b1b1b1;
    background-color: QLinearGradient(x1: 0,
    y1: 0,
    x2: 0,
    y2: 1,
    stop: 0 #565656,
    stop: 0.1 #525252,
    stop: 0.5 #4e4e4e,
    stop: 0.9 #4a4a4a,
    stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 0px;
    font-size: 16px;
    font-weight: bold;
    padding-left: 5px;
    padding-right: 5px;
}

QPushButton:pressed
{
    background-color: QLinearGradient(
    x1: 0,
    y1: 0,
    x2: 0,
    y2: 1,
    stop: 0 #2d2d2d,
    stop: 0.1 #2b2b2b,
    stop: 0.5 #292929,
    stop: 0.9 #282828,
    stop: 1 #252525);
}

QComboBox:hover,QPushButton:hover
{
    border: 2px solid QLinearGradient(
    x1: 0,
    y1: 0,
    x2: 0,
    y2: 1,
    stop: 0 #ffa02f,
    stop: 1 #d7801a);
}
"""


class SongButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(250, 100))
        self.setStyleSheet(BTN_STYLE)
        self.index = 0
        self.parent = parent
        self._fragment = None

    def __str__(self):
        return self.text()

    @property
    def fragment(self):
        return self._fragment

    def set_index(self, index):
        self.index = index

    def set_fragment(self, fragment):
        self._fragment = fragment
        self.setText(fragment.name)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        mime_data = FragmentMimeData()
        mime_data.set_fragment(self.fragment)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        if isinstance(self.parent, SoundContainer):
            self.parent.remove_sound(self.index)
            self.close()
        drop_action = drag.exec(QtCore.Qt.MoveAction)

        super().mouseMoveEvent(e)


class SoundContainer(QWidget):
    fragmentAdded = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.init_ui()
        self.sounds = []
        self.is_dragging = False
        self.insert_line_pos = 0
        self.index_to_insert = -1
        self.ext = ('.mp3', '.wav')
        self.resize(QSize(self.cur_width, self.h))

    def init_ui(self):
        self.top_padding = 5
        self.side_padding = 10
        self.sound_width = 250
        self.sound_height = 100
        self.sound_distance = 15

        self.h = 110

    @property
    def cur_width(self):
        width = (len(self.sounds)) *\
                (self.sound_width + self.sound_distance) + self.side_padding
        if width - self.side_padding == 0:
            width = self.parent().width() if self.parent() is not None else 500
        return width

    def add_fragment(self, fragment):
        if not isinstance(fragment, Fragment):
            raise ValueError
        sound = SongButton(self)
        sound.set_fragment(fragment)
        self.sounds.append(sound)
        self.rebuild()

    def insert_fragment(self, fragment, index):
        if not isinstance(fragment, Fragment):
            raise ValueError
        sound = SongButton(self)
        sound.set_fragment(fragment)
        self.sounds.insert(index, sound)
        self.rebuild()

    def remove_sound(self, index):
        self.sounds.pop(index)
        self.rebuild()

    def dragMoveEvent(self, e: QtGui.QMouseEvent):
        super().dragMoveEvent(e)
        if self.is_dragging:
            rect_width = self.sound_width + self.sound_distance
            x = int(e.pos().x())
            rect_num = x // rect_width
            rect_center = rect_width * rect_num + (self.sound_width / 2)
            rect_center += self.side_padding
            if rect_center < x:
                self.index_to_insert = rect_num + 1
                left_point = rect_center
                right_point = (left_point + self.sound_distance +
                               self.sound_width)
            else:
                self.index_to_insert = rect_num
                right_point = rect_center
                left_point = (right_point - self.sound_distance -
                              self.sound_width)
            self.insert_line_pos = (left_point + right_point) / 2
            self.update()

    def paintEvent(self, e: QtGui.QPaintEvent):
        super().paintEvent(e)
        if self.is_dragging:
            painter = QPainter(self)
            pen = QPen()
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(QLine(QPoint(self.insert_line_pos, 0),
                                   QPoint(self.insert_line_pos,
                                          self.sound_height + 6)))

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        self.is_dragging = True
        mime_data = e.mimeData()
        if mime_data.hasFormat("user/fragment"):
            e.accept()
        else:
            e.ignore()

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent):
        self.index_to_insert = -1
        self.insert_line_pos = -10
        self.update()

    def dropEvent(self, e: QtGui.QDropEvent):
        mime_data = e.mimeData()
        if mime_data.hasFormat("user/fragment"):
            sound = SongButton(self)
            sound.set_fragment(mime_data.fragment_data())
        self.insert_line_pos = -10
        self.update()

    def rebuild(self):
        self.resize(QSize(self.cur_width, self.h))

        for ind_sound in enumerate(self.sounds):
            index, sound = ind_sound
            x = self.side_padding
            x += index * (self.sound_width + self.sound_distance)
            y = self.top_padding
            sound.setGeometry(QRect(QPoint(x, y), QSize(self.sound_width,
                                                        self.sound_height)))
            sound.set_index(index)
            sound.show()

        self.fragmentAdded.emit(len(self.sounds))

    def clear(self):
        for sound in self.sounds:
            sound.close()
        self.sounds.clear()
        self.rebuild()


def main():
    pass


if __name__ == "__main__":
    main()
