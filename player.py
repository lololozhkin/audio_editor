import sys
import os
from PyQt5 import QtMultimedia
from PyQt5.QtWidgets import QListWidget, QAction, QMenu, \
    QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSlider, \
    QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, QUrl


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.statusBar()
        self.player = PlayerInside()
        self.init_ui()

        self.play_action.triggered.connect(self.load_track)

        self.delete_file.setShortcut('Del')
        self.delete_file.triggered.connect(
            lambda: self.delete_files(self.list_widget.selectedIndexes()))

        self.context_menu.addAction(self.play_action)
        self.context_menu.addAction(self.delete_file)

        self.open_file.setShortcut('Ctrl+O')
        self.open_file.triggered.connect(self.show_dialog)

        self.file_menu.addAction(self.open_file)

        self.list_widget.installEventFilter(self)

        self.addAction(self.delete_file)
        self.addAction(self.play_action)

        self.q_player.mediaStatusChanged.connect(self.init_player)
        self.q_player.stateChanged.connect(self.change_app_state)

        self.play_pause_button.clicked.connect(self.play_pause_on_clicked)
        self.stop_button.clicked.connect(self.q_player.stop)

        self.time_slider.valueChanged.connect(self.q_player.setPosition)
        self.volume_slider.valueChanged.connect(self.q_player.setVolume)

        self.q_player.positionChanged.connect(self.time_slider.setValue)
        self.q_player.volumeChanged.connect(self.volume_slider.setValue)

        self.q_player.setVolume(50)

        self.hbox.addWidget(self.play_pause_button)
        self.hbox.addWidget(self.stop_button)
        self.hbox.addWidget(self.volume_slider)

        self.vbox.addWidget(self.list_widget)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.time_slider)
        buf_widget = QWidget(self)
        buf_widget.setLayout(self.vbox)
        self.setCentralWidget(buf_widget)

        self.setGeometry(300, 300, 550, 500)
        self.setWindowTitle('Audio Player')
        self.show()

    def init_ui(self):
        self.menubar = self.menuBar()

        self.list_widget = QListWidget()

        self.open_file = QAction(QIcon('img/open.png'), 'Add file', self)
        self.open_file.setStatusTip('Open new file')

        self.delete_file = QAction(QIcon('img/delete.png'),
                                   'Delete file',
                                   self)
        self.delete_file.setStatusTip('Delete file from the list')

        self.file_menu = self.menubar.addMenu('File')

        self.play_action = QAction(QIcon('img/play.png'), 'Play file', self)
        self.play_action.setStatusTip('Play current file')

        self.context_menu = QMenu(self)

        self.vbox = QVBoxLayout(self)
        self.hbox = QHBoxLayout(self)

        self.play_pause_button = QPushButton(QIcon('img/play.png'),
                                             'Play',
                                             self)
        self.play_pause_button.setEnabled(False)
        self.stop_button = QPushButton(QIcon('img/stop.png'), 'Stop', self)
        self.stop_button.setEnabled(False)

        self.time_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.time_slider.setEnabled(False)
        self.volume_slider.setEnabled(False)
        self.time_slider.setMinimum(0)
        self.time_slider.setMinimum(0)

        self.q_player = QtMultimedia.QMediaPlayer()
        self.q_player.setNotifyInterval(2000)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.list_widget and event.type() == QEvent.ContextMenu:
            if obj.itemAt(event.pos()) is not None:
                self.context_menu.exec_(event.globalPos())
                return True
        return super().eventFilter(obj, event)

    def show_dialog(self):
        files_choose_string = 'All music files(*.mp3;*.wav);;' \
                              'MP3 files(*.mp3);;WAV files(*.wav)'
        file_names, _ = QFileDialog.getOpenFileNames(self,
                                                     'Add files',
                                                     '/home',
                                                     files_choose_string)
        if file_names:
            for file_name in file_names:
                self.player.add_file(file_name)
            self.list_widget.clear()
            for file_name in self.player.get_file_names():
                self.list_widget.addItem(file_name)

    def delete_files(self, indexes):
        if len(indexes) > 0:
            for index in indexes:
                self.player.remove_file(index.row())
            self.list_widget.clear()
            for file_name in self.player.get_file_names():
                self.list_widget.addItem(file_name)

    def init_player(self, state):
        if state == QtMultimedia.QMediaPlayer.LoadedMedia:
            self.q_player.stop()

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(True)

            self.stop_button.setEnabled(True)

            self.time_slider.setEnabled(True)
            self.time_slider.setMaximum(self.q_player.duration())

            self.volume_slider.setEnabled(True)

        elif state == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.q_player.stop()
            self.time_slider.setValue(0)

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(True)

            self.stop_button.setEnabled(False)

        elif (state == QtMultimedia.QMediaPlayer.InvalidMedia or
              state == QtMultimedia.QMediaPlayer.NoMedia):

            self.time_slider.setValue(0)
            self.time_slider.setEnabled(False)
            self.volume_slider.setEnabled(False)

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(False)

            self.stop_button.setEnabled(False)

    def change_app_state(self, state):
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            self.time_slider.setValue(0)
            self.stop_button.setEnabled(False)

            self.play_pause_button.setEnabled(True)
            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')

        elif state == QtMultimedia.QMediaPlayer.PausedState:
            self.stop_button.setEnabled(True)

            self.play_pause_button.setText('Play')
            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setEnabled(True)

        elif state == QtMultimedia.QMediaPlayer.PlayingState:
            self.stop_button.setEnabled(True)

            self.play_pause_button.setEnabled(True)
            self.play_pause_button.setIcon(QIcon('img/pause.png'))
            self.play_pause_button.setText('Pause')

    def play_pause_on_clicked(self):
        state = self.q_player.state()
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self.q_player.pause()
        else:
            self.q_player.play()

    def load_track(self):
        file_to_play = self.player.get_file_in_index(
            self.list_widget.currentRow())
        b = QUrl.fromLocalFile(file_to_play)
        a = QtMultimedia.QMediaContent(b)
        self.q_player.setMedia(a)


class PlayerInside:
    def __init__(self):
        self._music_files_list = []
        self._music_files_set = set()

    def add_file(self, file_dir):
        if file_dir not in self._music_files_set:
            self._music_files_list.append(file_dir)
            self._music_files_set.add(file_dir)

    def remove_file(self, position):
        file_dir = self._music_files_list[position]
        self._music_files_list.pop(position)
        self._music_files_set.remove(file_dir)

    def get_file_names(self):
        return map(lambda x: os.path.split(x)[1], self._music_files_list)

    def get_file_in_index(self, index):
        return self._music_files_list[index]


def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
