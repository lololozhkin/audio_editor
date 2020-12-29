from PyQt5.QtCore import QMimeData


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


def main():
    pass


if __name__ == "__main__":
    main()
