import sys
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, \
    QApplication, QDialog, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QUrl, QRect, QSize

from Fragment import Fragment
from TwoPointersSlider import TwoPointersSlider
from PlayerInside import PlayerInside
from FragmentPlayer import FragmentPlayer


class CutDialog(QDialog):
    fileCut = QtCore.pyqtSignal(Fragment)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.media_path = None
        self.player_inside = PlayerInside()
        self.cut_file_path = None
        self._fragment = None

        self.vbox.addWidget(self.cut_slider)
        self.vbox.addWidget(self.play_pause_button)

        self.hbox.addWidget(self.cut_button)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.cut_slider.mainSliderMoved.connect(self.on_mainSliderMoved)
        self.player.overriddenPositionChanged.connect(
            self.cut_slider.set_main_pos)

        self.cut_slider.endOfRange.connect(self.on_end_of_range)

        self.play_pause_button.clicked.connect(self.play_pause_on_clicked)
        self.cut_button.clicked.connect(self.on_cut_button_clicked)

        self.player.stateChanged.connect(self.on_state_changed)
        self.player.mediaStatusChanged.connect(self.init_player)

    def init_ui(self):
        self.cut_slider = TwoPointersSlider(self)
        self.play_pause_button = QPushButton(QIcon('img/play.png'),
                                             'Play',
                                             self)
        self.cut_button = QPushButton(QIcon('img/cut.png'),
                                      'Cut',
                                      self)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.player = FragmentPlayer()
        self.player.setNotifyInterval(5)

        self.setGeometry(QRect(300, 300, 500, 150))
        self.setWindowTitle("Cut file")
        self.setWindowIcon(QIcon('img/cut.png'))
        self.resize(QSize(500, 150))
        # self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def on_cut_button_clicked(self):
        ok, text = self.show_dialog()
        if ok:
            self.setCursor(QCursor(Qt.WaitCursor))
            self.play_pause_button.setEnabled(False)
            self.cut_button.setEnabled(False)

            fragment = Fragment(self.cut_slider.first_pointer_pos,
                                       self.cut_slider.second_pointer_pos,
                                       self._fragment)
            fragment.set_name(text)
            self.fileCut.emit(fragment)

            self.play_pause_button.setEnabled(True)
            self.cut_button.setEnabled(True)
            self.unsetCursor()

    def show_dialog(self):
        text, ok = QInputDialog.getText(self,
                                        'Enter fragment name',
                                        self._fragment.name)

        return ok, text

    def set_media(self, path):
        url = QUrl.fromLocalFile(path)
        media = QtMultimedia.QMediaContent(url)
        self.player.setMedia(media)
        self.media_path = path

    def set_fragment(self, fragment):
        self._fragment = fragment
        self.player.set_fragment(fragment)

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

        elif (state == QtMultimedia.QMediaPlayer.InvalidMedia or
              state == QtMultimedia.QMediaPlayer.NoMedia):

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(False)

    def on_mainSliderMoved(self, position):
        # self.player.pause()
        self.player.set_fragment_position(position)

    @staticmethod
    def get_path_for_os(path):
        if sys.platform.find('linux') != -1:
            return f'{path[0]}.{path[1][:3]}'
        else:
            return path[0]


def main():
    app = QApplication(sys.argv)
    ex = CutDialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
