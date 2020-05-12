from PyQt5.QtCore import QMimeData
from Fragment import Fragment


class FragmentMimeData(QMimeData):
    def __init__(self, parent=None):
        super().__init__()
        self._fragment = None
        self._my_formats = []

    def hasFormat(self, mimetype):
        return (mimetype in self._my_formats) or super().hasFormat(mimetype)

    def set_fragment(self, fragment):
        self._fragment = fragment
        self._my_formats = ["user/fragment"]

    def fragment_data(self):
        if self.hasFormat("user/fragment"):
            return self._fragment


PATH = r"D:\Downloads\nokiaarabicringtonenokiaarabicringtone_(st-tancpol.ru).mp3"


def main():
    a = FragmentMimeData()
    fragment = Fragment.parent_fragment(PATH)
    a.set_fragment(fragment)
    print(a.fragment_data())


if __name__ == "__main__":
    main()
