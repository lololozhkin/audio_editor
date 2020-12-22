from pydub import AudioSegment
import os
import re


class Fragment:
    _r = re.compile(r'\(is_parent:(?P<is_parent>.+?),'
                    r'source:(?P<source>.+?),'
                    r'name:(?P<name>.+?),'
                    r'start:(?P<start>.+?),'
                    r'end:(?P<end>.+?),'
                    r'parent:(?P<parent>.+)\)')

    def __init__(self, start, end, parent=None):
        self._parent = parent
        self._start = start
        self._end = end
        self._is_playing = False

        self._source_path = parent.source_path if parent is not None else None

        self._parent_absolute_start = parent.absolute_start \
            if parent is not None else 0
        self._parent_absolute_end = parent.absolute_end \
            if parent is not None else 0
        self._name = None

        self._is_parent = False

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

    def __repr__(self):
        return f'(is_parent:{self._is_parent},' \
               f'source:{self.source_path},' \
               f'name:{self.name},' \
               f'start:{self.start},' \
               f'end:{self.end},' \
               f'parent:{repr(self.parent)})'

    def is_parent(self):
        return self._is_parent

    @property
    def name(self):
        return self._name if self._name is not None else self.source_path

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

    @property
    def has_parent(self):
        return self._parent is not None

    @property
    def parent(self):
        if self._parent is None:
            return None

        fragment = Fragment(self._parent_absolute_start,
                            self._parent_absolute_end)
        fragment.set_source(self.source_path)
        return fragment

    @property
    def is_playing(self):
        return self._is_playing

    @is_playing.setter
    def is_playing(self, state):
        self._is_playing = state

    @property
    def shown_name(self):
        return self.name + ('     (Playing Now)' if self.is_playing else '')

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
        fragment._is_parent = True
        return fragment

    @staticmethod
    def from_repr(string):
        m = re.match(Fragment._r, string)
        is_parent = m['is_parent'] == 'True'
        source = m['source']

        if is_parent:
            return Fragment.parent_fragment(source)

        name = m['name']
        start = int(m['start'])
        end = int(m['end'])
        parent = None if m['parent'] == 'None' \
            else Fragment.from_repr(m['parent'])

        fragment = Fragment(start, end, parent)
        fragment.set_name(name)
        fragment.set_source(source)

        return fragment


def main():
    pass


if __name__ == '__main__':
    main()
