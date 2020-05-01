from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QPushButton,\
    QWidget, QScrollArea
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QSize
from PlayerInside import PlayerInside
from SoundContainer import SoundContainer
import sys


class ConcatenateWidget(QWidget):
    concatenate_finished = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        self.scroll_area.setWidget(self.container)

        self.concatenate_btn.clicked.connect(self.on_concatenate_clicked)
        self.concatenate_btn.setEnabled(False)

        self.container.fileAdded.connect(self.on_file_added)

        self.vbox.addWidget(self.scroll_area)
        self.vbox.addWidget(self.concatenate_btn, alignment=Qt.AlignRight)

        self.setLayout(self.vbox)

    def init_ui(self):
        self.scroll_area = QScrollArea(self)
        self.vbox = QVBoxLayout()
        self.container = SoundContainer()
        self.resize(QSize(1000, 180))
        self.setFixedHeight(180)
        self.concatenate_btn = QPushButton(self, text='Concatenate')
        self.concatenate_btn.resize(self.concatenate_btn.size().width(), 100)

    def add_path(self, path):
        self.container.add_sound(path)

    def on_file_added(self, files_amount):
        if files_amount >= 1:
            self.concatenate_btn.setEnabled(True)
        else:
            self.concatenate_btn.setEnabled(False)

    def on_concatenate_clicked(self):
        path = QFileDialog.getSaveFileName(parent=self,
                                           caption="Save file",
                                           filter="wav (*.wav);;mp3 (*.mp3)")
        if path[0] and path[1]:
            path = ConcatenateWidget.get_path_for_os(path)

            self.setCursor(QCursor(Qt.WaitCursor))
            self.concatenate_btn.setDisabled(True)

            PlayerInside.concatenate(map(lambda sound: sound.path,
                                         self.container.sounds),
                                     path)
            self.concatenate_btn.setEnabled(True)
            self.unsetCursor()

            self.container.clear()
            self.concatenate_finished.emit(path)

    @staticmethod
    def get_path_for_os(path):
        if sys.platform.find('linux') != -1:
            return f'{path[0]}.{path[1][:3]}'
        else:
            return path[0]
