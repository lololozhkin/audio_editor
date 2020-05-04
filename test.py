import sys
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtWidgets import QListWidget, QAction, QMenu, \
    QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSlider, \
    QMainWindow, QApplication, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, QUrl
from PlayerInside import PlayerInside
from CutDIalog import CutDialog
from ConcatenateWidget import ConcatenateWidget
from Fragment import Fragment
from FragmentPlayer import FragmentPlayer
import time


PATH = r"D:\Downloads\nokiaarabicringtonenokiaarabicringtone_(st-tancpol.ru).mp3"


def main():
    app = QApplication(sys.argv)
    ex = FragmentPlayer()
    fragment = Fragment.parent_fragment(PATH)
    ex.set_fragment(fragment)
    ex.setVolume(100)
    ex.play()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
