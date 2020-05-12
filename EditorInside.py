import os
import sys
from Fragment import Fragment

from pydub import AudioSegment


class EditorInside:
    path_to_tmp = os.path.join(os.getcwd(), 'tmp')
    formats = ('wav', 'mp3')

    try:
        os.mkdir(path_to_tmp)
    except Exception as e:
        pass

    def __init__(self):
        self._music_fragments_list = []

    def add_file_path(self, file_dir):
        fragment = Fragment.parent_fragment(file_dir)
        self._music_fragments_list.append(fragment)

    def add_fragment(self, fragment):
        self._music_fragments_list.append(fragment)

    def remove_fragment(self, position):
        self._music_fragments_list.pop(position)

    def get_fragments(self):
        return self._music_fragments_list

    def get_fragment_in_index(self, index):
        return self._music_fragments_list[index]

    @staticmethod
    def cut_fragment(parent, start, end, name='Result'):
        fragment = Fragment(start, end, parent)
        fragment.set_name(name)
        return fragment

    @staticmethod
    def concatenate(fragments, name='result'):
        segments = {}
        for fragment in fragments:
            if not (fragment.source_path in segments.keys()):
                path = fragment.source_path
                segments[path] = EditorInside._segment_from_file(path)
        result = AudioSegment.silent(0)
        for fragment in fragments:
            start, end = fragment.absolute_start, fragment.absolute_end
            path = fragment.source_path
            new_segment = segments[path][start:end]
            result = result + new_segment

        ext = os.path.splitext(name)[1][1:]
        if not ext or not (ext in EditorInside.formats):
            ext = 'wav'
        path = os.path.join(EditorInside.path_to_tmp, name)
        result.export(path, format=ext)

        fragment = Fragment.parent_fragment(path)
        fragment.set_name(name)
        return fragment

    @staticmethod
    def save_fragment(fragment, path):
        segment = EditorInside._segment_from_file(fragment.source_path)
        segment = segment[fragment.absolute_start:fragment.absolute_end]
        EditorInside._segment_export(segment, path)

    @staticmethod
    def _segment_from_file(path):
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = 'wav'
        else:
            ext = ext[1:]
        return AudioSegment.from_file(path, format=ext)

    @staticmethod
    def _segment_export(segment, path):
        ext = os.path.splitext(path)[1]
        if not ext:
            ext = 'wav'
        else:
            ext = ext[1:]

        segment.export(path, format=ext)



def main():
    print(sys.platform)
    path = 'abacaba.wav'
    print(os.path.splitext(path))


if __name__ == '__main__':
    main()
