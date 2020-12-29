from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, \
    QWidget, QScrollArea, QInputDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QSize
from EditorInside import EditorInside
from SoundContainer import SoundContainer
from Fragment import Fragment


class ConcatenateWidget(QWidget):
    concatenate_finished = QtCore.pyqtSignal(Fragment)

    def __init__(self, parent=None, fragments=None):
        super().__init__(parent)
        if fragments is None:
            fragments = []
        self.fragments = fragments

        self.init_ui()

        self.scroll_area.setWidget(self.container)

        self.concatenate_btn.clicked.connect(self.on_concatenate_clicked)
        self.concatenate_btn.setEnabled(False)

        self.container.fragmentAdded.connect(self.on_fragment_added)

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

    def add_fragment(self, fragment):
        self.container.add_fragment(fragment)

    def on_fragment_added(self, files_amount):
        if files_amount >= 1:
            self.concatenate_btn.setEnabled(True)
        else:
            self.concatenate_btn.setEnabled(False)

    def on_concatenate_clicked(self):
        input_text = 'Enter fragment name'
        last_name = 'fragment.wav'
        while True:
            name, ok = QInputDialog.getText(self,
                                            'Fragment name',
                                            input_text,
                                            text=last_name)

            if ok:
                if name in (fragment.name for fragment in self.fragments):
                    input_text = 'Enter fragment name again.'
                    last_name = name
                    continue

                self.setCursor(QCursor(Qt.WaitCursor))
                self.concatenate_btn.setDisabled(True)

                fragments = (snd.fragment for snd in self.container.sounds)
                fragment = EditorInside.concatenate(list(fragments), name)

                self.concatenate_btn.setEnabled(True)
                self.unsetCursor()

                self.container.clear()
                self.concatenate_finished.emit(fragment)
                break
            else:
                break

    def get_fragments(self):
        return self.container.get_fragments()
