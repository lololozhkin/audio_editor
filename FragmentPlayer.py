from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtCore import QUrl


class FragmentPlayer(QtMultimedia.QMediaPlayer):
    overriddenPositionChanged = QtCore.pyqtSignal(int)
    endOfMedia = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.positionChanged.connect(self._on_position_changed)
        self.endOfMedia.connect(self._on_end_of_media)
        self._fragment = None

    def set_fragment(self, fragment):
        self._fragment = fragment
        url = QUrl.fromLocalFile(self._fragment.source_path)
        media = QtMultimedia.QMediaContent(url)
        self.setMedia(media)
        self.set_fragment_position(0)

    def stop(self):
        if self.state() in (QtMultimedia.QMediaPlayer.StoppedState, QtMultimedia.QMediaPlayer.PausedState):
            return
        super().stop()
        self.set_fragment_position(0)
        self.pause()

    def duration(self):
        return self._fragment.duration

    def _on_position_changed(self, position):
        print(position)
        if self._fragment is not None:
            calculated_pos = position - self._fragment.absolute_start

            if calculated_pos >= self._fragment.duration:
                self.endOfMedia.emit()
            self.overriddenPositionChanged.emit(calculated_pos)

    def set_fragment_position(self, position):
        self.setPosition(self._fragment.absolute_start + position)

    def _on_end_of_media(self):
        self.stop()
