from pydub import AudioSegment
import os

class Fragment:
    def __init__(self, start, end, parent=None):
        self._parent = parent
        self._start = start
        self._end = end

        self._source_path = parent.source_path if parent is not None else None
        self._parent_absolute_start = parent.absolute_start \
            if parent is not None else 0

    @property
    def source_path(self):
        return self._source_path

    @property
    def absolute_start(self):
        return self._parent_absolute_start + self.start

    @property
    def duration(self):
        return self._end - self._start

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def set_start(self, start):
        self._start = start

    def set_end(self, end):
        self._end = end

    def set_source(self, source):
        self._source_path = source

    @staticmethod
    def parent_fragment(source):
        formating = os.path.splitext(source)[1][1:]
        duration = len(AudioSegment.from_file(source, format=formating))

        fragment = Fragment(0, duration, None)
        fragment.set_source(source)

