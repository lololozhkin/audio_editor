import os
import sys

from pydub import AudioSegment


class PlayerInside:
    def __init__(self):
        self._music_files_list = []
        self._music_files_set = set()

        try:
            os.mkdir('tmp')
            self.path_to_tmp = os.path.join(os.getcwd(), 'tmp')
        except FileExistsError as e:
            self.path_to_tmp = os.path.join(os.getcwd(), 'tmp')

    def add_file(self, file_dir):
        if file_dir not in self._music_files_set:
            self._music_files_list.append(file_dir)
            self._music_files_set.add(file_dir)

    def remove_file(self, position):
        file_dir = self._music_files_list[position]
        self._music_files_list.pop(position)
        self._music_files_set.remove(file_dir)

    def get_file_names(self):
        return map(lambda x: os.path.split(x)[1], self._music_files_list)

    def get_file_in_index(self, index):
        return self._music_files_list[index]

    def cut_file(self, file_path, start, end, path_to_save):
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

