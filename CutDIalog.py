import sys
from PyQt5 import QtMultimedia, QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, \
    QApplication, QDialog, QFileDialog
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QUrl, QRect, QSize
from TwoPointersSlider import TwoPointersSlider
from PlayerInside import PlayerInside


class CutDialog(QDialog):
    fileCut = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.media_path = None
        self.player_inside = PlayerInside()
        self.cut_file_path = None

        self.vbox.addWidget(self.cut_slider)
        self.vbox.addWidget(self.play_pause_button)

        self.hbox.addWidget(self.cut_button)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.cut_slider.mainSliderMoved.connect(self.on_mainSliderMoved)
        self.player.positionChanged.connect(self.cut_slider.set_main_pos)

        self.cut_slider.endOfRange.connect(self.on_end_of_range)

        self.play_pause_button.clicked.connect(self.play_pause_on_clicked)
        self.cut_button.clicked.connect(self.on_cut_button_clicked)

        self.player.stateChanged.connect(self.on_state_changed)
        self.player.durationChanged.connect(self.cut_slider.set_maximum)
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

        self.player = QtMultimedia.QMediaPlayer()
        self.player.setNotifyInterval(5)

        self.setGeometry(QRect(300, 300, 500, 150))
        self.setWindowTitle("Cut file")
        self.setWindowIcon(QIcon('img/cut.png'))
        self.resize(QSize(500, 150))
        # self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(Qt.Window, True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

    def on_cut_button_clicked(self):
        path = QFileDialog.getSaveFileName(parent=self,
                                           caption="Save file",
                                           filter="wav (*.wav);;mp3 (*.mp3)")
        if path[0] and path[1]:
            self.setCursor(QCursor(Qt.WaitCursor))
            self.play_pause_button.setEnabled(False)
            self.cut_button.setEnabled(False)

            self.player_inside.cut_file(self.media_path,
                                        self.cut_slider.first_pointer_pos,
                                        self.cut_slider.second_pointer_pos,
                                        CutDialog.get_path_for_os(path))

            self.play_pause_button.setEnabled(True)
            self.cut_button.setEnabled(True)
            self.unsetCursor()

            self.fileCut.emit(CutDialog.get_path_for_os(path))

    def set_media(self, path):
        url = QUrl.fromLocalFile(path)
        media = QtMultimedia.QMediaContent(url)
        self.player.setMedia(media)
        self.media_path = path

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
            self.player.setPosition(self.cut_slider.main_pointer_pos)

        elif (state == QtMultimedia.QMediaPlayer.InvalidMedia or
              state == QtMultimedia.QMediaPlayer.NoMedia):

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(False)

    def on_mainSliderMoved(self, position):
        # self.player.pause()
        self.player.setPosition(position)

    @staticmethod
    def get_path_for_os(path):
        if sys.platform.find('linux') != -1:
            return f'{path[0]}.{path[1][:3]}'
        else:
            return path[0]


def main():
    app = QApplication(sys.argv)
    ex = CutDialog()
    ex.set_media(
        r"D:\PythonTask\nokiaarabicringtonenokiaarabicringtone_(st-tancpol.ru).mp3")
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
