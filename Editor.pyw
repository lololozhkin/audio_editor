import sys
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtWidgets import QListWidget, QAction, QMenu, \
    QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSlider, \
    QMainWindow, QApplication, QListWidgetItem, QSpinBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject
from EditorInside import EditorInside
from CutDIalog import CutDialog
from ConcatenateWidget import ConcatenateWidget
from FragmentPlayer import FragmentPlayer
from Fragment import Fragment


class Editor(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.statusBar()
        self.editor = EditorInside()
        self.init_ui()

        self.play_action.triggered.connect(self.load_track)

        self.delete_file.setShortcut('Del')
        self.delete_file.triggered.connect(
            lambda: self.delete_fragments(self.list_widget.selectedIndexes())
        )

        self.cut_file.setShortcut('Ctrl+K')
        self.cut_file.triggered.connect(self.on_cut_file)

        self.concatenate_action.triggered.connect(self.on_concatenate)

        self.edit_cut_action.triggered.connect(self.on_edit_cut)

        self.save_action.triggered.connect(self.on_save_triggered)

        self.context_menu.addAction(self.play_action)
        self.context_menu.addAction(self.cut_file)
        self.context_menu.addAction(self.edit_cut_action)
        self.context_menu.addAction(self.concatenate_action)
        self.context_menu.addAction(self.save_action)
        self.context_menu.addAction(self.delete_file)

        self.open_file.setShortcut('Ctrl+O')
        self.open_file.triggered.connect(self.show_dialog)

        self.file_menu.addAction(self.open_file)

        self.open_project_action.triggered.connect(self.on_open_project)
        self.save_project_action.triggered.connect(self.on_save_project)

        self.project_menu.addAction(self.open_project_action)
        self.project_menu.addAction(self.save_project_action)

        self.list_widget.installEventFilter(self)
        self.list_widget.itemDoubleClicked.connect(
            lambda item: self.load_track()
        )

        self.addAction(self.delete_file)
        self.addAction(self.play_action)

        self.q_player.mediaStatusChanged.connect(self.init_player)
        self.q_player.stateChanged.connect(self.change_app_state)

        self.play_pause_button.clicked.connect(self.play_pause_on_clicked)
        self.stop_button.clicked.connect(self.q_player.stop)

        self.time_slider.sliderMoved.connect(
            self.q_player.set_fragment_position
        )

        self.volume_slider.valueChanged.connect(self.q_player.setVolume)

        self.q_player.overriddenPositionChanged.connect(
            self.time_slider.setValue
        )
        self.q_player.volumeChanged.connect(self.volume_slider.setValue)

        self.timecode.valueChanged.connect(self.on_timecode_value_changed)
        self.time_slider.valueChanged.connect(self.timecode.setValue)

        self.q_player.setVolume(50)

        self.concatenate_widget.concatenate_finished.connect(self.concatenate)

        self.hbox.addWidget(self.play_pause_button)
        self.hbox.addWidget(self.stop_button)
        self.hbox.addWidget(self.volume_slider)

        self.vbox.addWidget(self.list_widget)
        self.vbox.addWidget(self.timecode)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.time_slider)
        self.vbox.addWidget(self.concatenate_widget)
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

        self.cut_file = QAction(QIcon('img/cut.png'), 'Cut file', self)
        self.cut_file.setStatusTip('Cut file')

        self.delete_file = QAction(
            QIcon('img/delete.png'),
            'Delete file',
            self
        )
        self.delete_file.setStatusTip('Delete file from the list')

        self.file_menu = self.menubar.addMenu('File')
        self.project_menu = self.menubar.addMenu('Project')

        self.save_project_action = QAction(
            QIcon('img/save_as.png'),
            'Save project',
            self
        )
        self.open_project_action = QAction(
            QIcon('img/open.png'),
            'Open project',
            self
        )

        self.play_action = QAction(QIcon('img/play.png'), 'Play file', self)
        self.play_action.setStatusTip('Play current file')

        self.concatenate_action = QAction(
            QIcon('img/concatenate'),
            'Add to concatenate list',
            self
        )
        self.concatenate_action.setStatusTip('Add to concatenate list')

        self.edit_cut_action = QAction(
            QIcon('img/cut.png'),
            'Edit file cutting',
            self
        )
        self.edit_cut_action.setStatusTip('Edit range of file cutting')

        self.save_action = QAction(
            QIcon('img/save_as.png'),
            'Save fragment',
            self
        )

        self.concatenate_widget = ConcatenateWidget(
            self,
            self.editor.fragments()
        )

        self.context_menu = QMenu(self)

        self.vbox = QVBoxLayout(self)
        self.hbox = QHBoxLayout(self)

        self.play_pause_button = QPushButton(
            QIcon('img/play.png'),
            'Play',
            self
        )
        self.play_pause_button.setEnabled(False)
        self.stop_button = QPushButton(QIcon('img/stop.png'), 'Stop', self)
        self.stop_button.setEnabled(False)

        self.time_slider = QSlider(Qt.Horizontal, self)
        self.time_slider.setStyleSheet("""
                    QSlider::groove:horizontal {
                        height: 10px;
                        margin: 0px;
                        border-radius: 5px;
                        background: #B0AEB1;
                    }
                    QSlider::handle:horizontal {
                        background: #fff;
                        border: 1px solid #E3DEE2;
                        width: 17px;
                        margin: -5px 0;
                        border-radius: 8px;
                    }
                    QSlider::sub-page:qlineargradient {
                        background: #FAA9A7;
                        border-radius: 5px;
                    }
                """)
        self.volume_slider = QSlider(Qt.Horizontal, self)

        self.time_slider.setEnabled(False)
        self.volume_slider.setEnabled(False)

        self.time_slider.setMinimum(0)
        self.volume_slider.setMinimum(0)

        self.timecode = QSpinBox(self)
        self.timecode.setMinimum(0)
        self.timecode.setSuffix(' ms')
        self.timecode.setEnabled(False)

        self.q_player = FragmentPlayer()
        self.q_player.setNotifyInterval(1)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.list_widget:
            if event.type() == QEvent.ContextMenu \
                    and obj.itemAt(event.pos()) is not None:
                if obj.itemAt(event.pos()).data(Qt.UserRole).is_parent():
                    a = QListWidgetItem()
                    self.edit_cut_action.setEnabled(False)
                else:
                    self.edit_cut_action.setEnabled(True)
                self.context_menu.exec_(event.globalPos())
                return True

        return super().eventFilter(obj, event)

    def show_dialog(self):
        files_choose_string = 'All music files(*.mp3 *.wav);;' \
                              'MP3 files(*.mp3);;WAV files(*.wav)'
        file_names = QFileDialog.getOpenFileNames(
            self,
            caption='Add files',
            filter=files_choose_string
        )
        file_names = set(file_names[0])
        existing_files = set(
            fragment.name for fragment in self.editor.fragments()
        )
        file_names -= existing_files
        if file_names:
            self.add_files(file_names)

    def add_files(self, file_names):
        if file_names:
            for file_name in file_names:
                self.editor.add_file_path(file_name)
            self.list_update()

    def add_fragment(self, fragment):
        self.editor.add_fragment(fragment)
        self.list_update()

    def delete_fragments(self, indexes):
        if len(indexes) > 0:
            for index in indexes:
                self.editor.remove_fragment(index.row())
            self.list_update()

    def clear(self):
        self.editor.clear()
        self.concatenate_widget.container.clear()
        self.list_update()

    def remove_fragment(self, index):
        self.editor.remove_fragment(index)
        self.list_update()

    def list_update(self):
        self.list_widget.clear()
        for fragment in self.editor.get_fragments():
            list_item = QListWidgetItem(self.list_widget)
            list_item.setData(Qt.UserRole, fragment)
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(
                list_item,
                QLabel(fragment.shown_name)
            )

    def init_player(self, state):
        if state == QtMultimedia.QMediaPlayer.LoadedMedia:
            self.q_player.pause()

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(True)
            self.timecode.setEnabled(True)

            self.stop_button.setEnabled(True)

            self.time_slider.setEnabled(True)
            self.time_slider.setMaximum(self.q_player.duration())
            self.timecode.setMaximum(self.q_player.duration())

            self.volume_slider.setEnabled(True)

            self.q_player.set_fragment_position(0)
            self.q_player.play()

        elif state == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.q_player.stop()
            self.time_slider.setValue(0)

            self.play_pause_button.setIcon(QIcon('img/play.png'))
            self.play_pause_button.setText('Play')
            self.play_pause_button.setEnabled(True)
            self.timecode.setEnabled(True)

            self.stop_button.setEnabled(False)

        elif (state == QtMultimedia.QMediaPlayer.InvalidMedia
              or state == QtMultimedia.QMediaPlayer.NoMedia):

            self.time_slider.setValue(0)
            self.time_slider.setEnabled(False)
            self.volume_slider.setEnabled(False)
            self.timecode.setEnabled(False)

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
        fragment = self.editor.get_fragment_in_index(
            self.list_widget.currentRow()
        )
        for f in self.editor.fragments():
            f.is_playing = False
        fragment.is_playing = True
        self.list_update()
        self.q_player.set_fragment(fragment)

    def on_edit_cut(self):
        self.q_player.pause()
        index = self.list_widget.currentRow()
        fragment = self.editor.get_fragment_in_index(index)
        cut_dialog = CutDialog(self)
        cut_dialog.set_fragment_for_editing(fragment)
        cut_dialog.setWindowModality(Qt.WindowModal)
        cut_dialog.fileCut.connect(
            lambda fragm: self.on_fileCut(fragm, cut_dialog, index)
        )
        cut_dialog.show()
        cut_dialog.exec_()

    def on_fileCut(self, fragment, dialog, index):
        self.add_fragment(fragment)
        dialog.close()
        self.remove_fragment(index)

    def on_cut_file(self):
        self.q_player.pause()
        fragment = self.editor.get_fragment_in_index(
            self.list_widget.currentRow())
        cut_dialog = CutDialog(self, self.editor.fragments())
        cut_dialog.set_fragment(fragment)
        cut_dialog.setWindowModality(Qt.WindowModal)
        cut_dialog.fileCut.connect(self.add_fragment)
        cut_dialog.show()
        cut_dialog.exec_()

    def on_concatenate(self):
        fragment_to_add = self.list_widget.selectedItems()[0].data(Qt.UserRole)
        self.concatenate_widget.add_fragment(fragment_to_add)

    def concatenate(self, fragment):
        self.add_fragment(fragment)

    def on_timecode_value_changed(self, value):
        self.time_slider.setValue(value)
        if self.q_player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.q_player.set_fragment_position(self.time_slider.value())

    def on_save_triggered(self):
        fragment = self.editor.get_fragment_in_index(
            self.list_widget.currentRow())
        path, ext = QFileDialog.getSaveFileName(self,
                                                'Save File',
                                                filter='*.wav;;*.mp3')
        if path and ext:
            path = f'{path}{ext[1:]}'
            EditorInside.save_fragment(fragment, path)

    def on_open_project(self):
        file = QFileDialog.getOpenFileName(self,
                                           'Open project',
                                           filter='Editor File(*.edf)')
        file = file[0]
        if file:
            self.clear()
            in_list = True
            with open(file, 'r') as f:
                for line in f:
                    if not line:
                        continue

                    if line.strip() == '---':
                        in_list = False
                        continue

                    if in_list:
                        self.add_fragment(Fragment.from_repr(line.strip()))
                    else:
                        self.concatenate_widget.add_fragment(
                            Fragment.from_repr(line.strip())
                        )

    def on_save_project(self):
        file, ext = QFileDialog.getSaveFileName(self,
                                                'Save project',
                                                filter='*.edf')
        file = EditorInside.dir_for_os(file, ext[1:])

        if file:
            with open(file, 'w') as f:
                for fragment in self.editor.fragments():
                    f.write(repr(fragment) + '\n')

                f.write('---\n')

                for fragment in self.concatenate_widget.get_fragments():
                    f.write(repr(fragment) + '\n')


def main():
    app = QApplication(sys.argv)
    ex = Editor()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
