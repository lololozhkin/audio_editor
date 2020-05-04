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
        self._name = None

    def __str__(self):
        return f'({self.source_path}, {self.start}, {self.end})'

    def __eq__(self, other):
        if isinstance(other, Fragment):
            return self.source_path == other.source_path \
                   and self.absolute_start == other.absolute_start \
                   and self.duration == other.duration
        else:
            return NotImplemented

    def __hash__(self):
        return self.name.__hash__() \
               ^ (self.absolute_start * 397) \
               ^ (self.duration * 179)

    @property
    def name(self):
        return self._name if self._name is not None\
            else os.path.split(self.source_path)[1]

    @property
    def source_path(self):
        return self._source_path

    @property
    def absolute_start(self):
        return self._parent_absolute_start + self.start

    @property
    def absolute_end(self):
        return self._parent_absolute_start + self.end

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

    def set_name(self, name):
        self._name = name

    @staticmethod
    def parent_fragment(source):
        formating = os.path.splitext(source)[1][1:]
        duration = len(AudioSegment.from_file(source, format=formating))

        fragment = Fragment(0, duration, None)
        fragment.set_source(source)
        return fragment

