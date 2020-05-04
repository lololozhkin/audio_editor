import os
import sys
from Fragment import Fragment

from pydub import AudioSegment


class PlayerInside:
    def __init__(self):
        self._music_fragments_list = []

    def add_file_path(self, file_dir):
        fragment = Fragment.parent_fragment(file_dir)
        self._music_fragments_list.append(fragment)

    def add_fragment(self, fragment):
        self._music_fragments_list.append(fragment)

    def remove_file(self, position):
        self._music_fragments_list.pop(position)

    def get_fragments(self):
        return self._music_fragments_list

    def get_fragment_in_index(self, index):
        return self._music_fragments_list[index]

    @staticmethod
    def cut_file(file_path, start, end, path_to_save):
        start, end = map(int, (start, end))
        formating = os.path.splitext(file_path)[1][1:]
        segment = AudioSegment.from_file(file_path,
                                         format=formating)
        segment = segment[start:end]

        save_path, ext = os.path.splitext(path_to_save)
        ext = ext[1:]

        segment.export(path_to_save, format=ext)

    @staticmethod
    def concatenate(iterible_urls, path):
        concatenated = AudioSegment.silent(0)
        save_path, ext = os.path.splitext(path)
        save_path = os.path.abspath(save_path)
        ext = ext[1:]
        for file_path in iterible_urls:
            file_path = PlayerInside.get_normal_path(file_path)
            file_path = os.path.abspath(file_path)
            file_format = os.path.splitext(file_path)[1][1:]
            cur_segment = AudioSegment.from_file(file_path, file_format)
            concatenated = concatenated + cur_segment
        concatenated.export(f'{save_path}.{ext}', format=ext)

    @staticmethod
    def get_normal_path(path):
        if sys.platform.find('linux') != -1:
            return path
        else:
            return path[1:]


def main():
    print(sys.platform)


if __name__ == '__main__':
    main()
