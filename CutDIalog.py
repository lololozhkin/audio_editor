import sys
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, \
    QApplication, QDialog, QInputDialog, QSpinBox
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QUrl, QRect, QSize

from Fragment import Fragment
from TwoPointersSlider import TwoPointersSlider
from EditorInside import EditorInside
from FragmentPlayer import FragmentPlayer


class CutDialog(QDialog):
    fileCut = QtCore.pyqtSignal(Fragment)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.player_inside = EditorInside()
        self.parent_fragment = None
        self._fragment = None
        self.editing = False

        self.set_pos_btns.addWidget(self.left_to_main)
        self.set_pos_btns.addWidget(self.right_to_main)

        self.time_codes_box.addWidget(self.left_time_code)
        self.time_codes_box.addWidget(self.main_time_code)
        self.time_codes_box.addWidget(self.right_time_code)

        self.vbox.addLayout(self.time_codes_box)
        self.vbox.addWidget(self.cut_slider)
        self.vbox.addLayout(self.set_pos_btns)
        self.vbox.addWidget(self.play_pause_button)
        self.vbox.addWidget(self.cut_button)

        self.left_to_main.clicked.connect(self.on_left_to_main_clicked)
        self.right_to_main.clicked.connect(self.on_right_to_main_clicked)

        self.left_time_code.valueChanged.connect(self.on_left_time_changed)
        self.right_time_code.valueChanged.connect(self.on_right_time_changed)
        self.main_time_code.valueChanged.connect(self.on_main_time_changed)

        self.cut_slider.leftPosChanged.connect(self.on_left_pos_changed)
        self.cut_slider.rightPosChanged.connect(self.on_right_pos_changed)
        self.cut_slider.mainPosChanged.connect(self.on_main_pos_changed)

        self.setLayout(self.vbox)

        self.cut_slider.mainSliderMoved.connect(self.on_mainSliderMoved)
        self.player.overriddenPositionChanged.connect(
            self.cut_slider.set_main_pos)

        self.cut_slider.endOfRange.connect(self.on_end_of_range)

        self.play_pause_button.clicked.connect(self.play_pause_on_clicked)
        self.cut_button.clicked.connect(self.on_cut_button_clicked)

        self.player.stateChanged.connect(self.on_state_changed)
        self.player.mediaStatusChanged.connect(self.init_player)
        self.player.durationChanged.connect(
            lambda x: self.cut_slider.set_maximum(self.player.duration()))

    def init_ui(self):
        self.cut_slider = TwoPointersSlider(self)
        self.play_pause_button = QPushButton(QIcon('img/play.png'),
                                             'Play',
                                             self)
        self.cut_button = QPushButton(QIcon('img/cut.png'),
                                      'Cut',
                                      self)
        self.vbox = QVBoxLayout()
        self.set_pos_btns = QHBoxLayout()
        self.time_codes_box = QHBoxLayout()

        self.player = FragmentPlayer()
        self.player.setNotifyInterval(5)

        self.right_time_code = QSpinBox(self)
        self.right_time_code.setSuffix(' ms')
        self.left_time_code = QSpinBox(self)
        self.left_time_code.setSuffix(' ms')
        self.main_time_code = QSpinBox(self)
        self.main_time_code.setSuffix(' ms')

        self.right_to_main = QPushButton(text='Set end', parent=self)
        self.left_to_main = QPushButton(text='Set start', parent=self)

        self.setGeometry(QRect(300, 300, 750, 200))
        self.setWindowTitle("Cut file")
        self.setWindowIcon(QIcon('img/cut.png'))
        self.setWindowFlag(Qt.Window, True)
        self.setFixedHeight(200)
        self.setMinimumWidth(750)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def on_cut_button_clicked(self):
        ok, text = self.show_dialog()
        if ok:
            self.setCursor(QCursor(Qt.WaitCursor))
            self.play_pause_button.setEnabled(False)
            self.cut_button.setEnabled(False)

            parent = self._fragment if not self.editing \
                else self.parent_fragment
            start = self.cut_slider.first_pointer_pos
            end = self.cut_slider.second_pointer_pos
            fragm = EditorInside.cut_fragment(parent, start, end, text)
            self.fileCut.emit(fragm)

            self.play_pause_button.setEnabled(True)
            self.cut_button.setEnabled(True)
            self.unsetCursor()

    def show_dialog(self):
        text, ok = QInputDialog.getText(self,
                                        'Fragment name',
                                        'Enter fragment name',
                                        text=self._fragment.name)

        return ok, text

    def set_fragment(self, fragment):
        self._fragment = fragment
        self.player.set_fragment(fragment)
        # self.cut_slider.set_maximum(self._fragment.duration)

    def set_fragment_for_editing(self, fragment):
        self._fragment = fragment
        self.parent_fragment = fragment.parent
        self.player.set_fragment(self.parent_fragment)
        self.editing = True
        self.cut_button.setText('Edit')

    def on_state_changed(self, state):
        if state == QtMultimedia.QMediaPlayer.PausedState:
            self.play_pause_button.setText('Play')
            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setEnabled(True)

        elif state == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_pause_button.setEnabled(True)
            self.play_pause_button.setIcon(QIcon('img/pause.png'))
            self.play_pause_button.setText('Pause')

    def play_pause_on_clicked(self):
        state = self.player.state()
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
        elif not self.cut_slider.end_of_range_check():
            self.player.play()

    def on_end_of_range(self):
        if not self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.player.pause()

    def init_player(self, state):
        if state == QtMultimedia.QMediaPlayer.LoadedMedia:
            self.player.stop()

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(True)

            self.cut_slider.set_maximum(self.player.duration())

            self.main_time_code.setMaximum(self.player.duration())
            self.right_time_code.setMaximum(self.player.duration())
            self.left_time_code.setMaximum(self.player.duration())

            if self.editing:
                self.cut_slider.set_left_pos(self._fragment.start)
                self.cut_slider.set_right_pos(self._fragment.end)

            self.main_time_code.setValue(self.cut_slider.main_pointer_pos)
            self.right_time_code.setValue(self.cut_slider.second_pointer_pos)
            self.left_time_code.setValue(self.cut_slider.first_pointer_pos)

        elif (state == QtMultimedia.QMediaPlayer.InvalidMedia or
              state == QtMultimedia.QMediaPlayer.NoMedia):

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(False)

    def closeEvent(self, e):
        self.player.stop()
        e.accept()

    def on_mainSliderMoved(self, position):
        # self.player.pause()
        self.player.set_fragment_position(position)

    def on_main_pos_changed(self, pos):
        self.main_time_code.setValue(pos)

    def on_left_to_main_clicked(self):
        self.cut_slider.set_left_pos(self.cut_slider.main_pointer_pos)

    def on_right_to_main_clicked(self):
        self.cut_slider.set_right_pos(self.cut_slider.main_pointer_pos)

    def on_left_time_changed(self, pos):
        self.cut_slider.set_left_pos(pos)
        self.main_time_code.setMinimum(pos)

    def on_right_time_changed(self, pos):
        self.cut_slider.set_right_pos(pos)
        self.main_time_code.setMaximum(pos)

    def on_left_pos_changed(self, pos):
        self.left_time_code.setValue(pos)
        self.right_time_code.setMinimum(pos)
        self.main_time_code.setMinimum(pos)

    def on_right_pos_changed(self, pos):
        self.right_time_code.setValue(pos)
        self.left_time_code.setMaximum(pos)
        self.main_time_code.setMaximum(pos)

    def on_main_time_changed(self, pos):
        self.cut_slider.set_main_pos(pos)
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.player.set_fragment_position(pos)


def main():
    app = QApplication(sys.argv)
    ex = CutDialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
