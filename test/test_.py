import sys
import os
import wave
import contextlib
from pydub import AudioSegment

sys.path.append('../')
sys.path.append('./')

from Fragment import Fragment
from EditorInside import EditorInside

PATH = os.path.join(os.getcwd(), 'test', 'abacaaba.wav')
try:
    AudioSegment.silent(10000).export(PATH, format='wav')
except Exception as e:
    pass


def get_wav_duration(path):
    with contextlib.closing(wave.open(path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration * 1000


class TestFragment:
    main_fragment = Fragment.parent_fragment(PATH)

    def test_creation(self):
        fragment = Fragment(0, 100, TestFragment.main_fragment)
        assert fragment is not None

    def test_duration(self):
        fragment = Fragment(0, 100, TestFragment.main_fragment)
        assert fragment.duration == 100

    def test_source(self):
        fragment = Fragment(0, 100, TestFragment.main_fragment)
        assert fragment.source_path == PATH

    def test_absolute_positions(self):
        fragment = Fragment(100, 1000, TestFragment.main_fragment)
        assert fragment.absolute_start == 100
        assert fragment.absolute_end == 1000

    def test_nesting_source(self):
        first_fragment = Fragment(100, 1000, TestFragment.main_fragment)
        second_fragment = Fragment(10, 20, first_fragment)
        assert second_fragment.source_path == PATH

    def test_nesting_absolute_positions(self):
        first_fragment = Fragment(100, 1000, TestFragment.main_fragment)
        second_fragment = Fragment(10, 20, first_fragment)
        assert second_fragment.absolute_start == 110
        assert second_fragment.absolute_end == 120

    def test_parent_creation(self):
        assert abs(get_wav_duration(PATH)
                   - TestFragment.main_fragment.duration) < 1

    def test_from_repr(self):
        pass


class TestOperations:
    def test_concatenate(self):
        try:
            first_path = os.path.join(os.getcwd(), 'test', 'first.wav')
            AudioSegment.silent(10000).export(first_path, 'wav')
            first = Fragment.parent_fragment(first_path)
        except Exception as e:
            pass

        try:
            second_path = os.path.join(os.getcwd(), 'test', 'second.wav')
            AudioSegment.silent(5000).export(second_path, 'wav')
            second = Fragment.parent_fragment(second_path)
        except Exception as e:
            pass

        fragment = EditorInside.concatenate([first, second])

        assert abs(fragment.duration - 15000) < 1

        concatenate_path = os.path.join(os.getcwd(), 'test', 'concatenate.wav')
        EditorInside.save_fragment(fragment, concatenate_path)

        assert abs(get_wav_duration(concatenate_path) - 15000) < 1

    def test_cut(self):
        try:
            first_path = os.path.join(os.getcwd(), 'test', 'first.wav')
            AudioSegment.silent(10000).export(first_path, 'wav')
            first = Fragment.parent_fragment(first_path)
        except Exception as e:
            pass

        fragment = EditorInside.cut_fragment(first, 1000, 9000)

        assert abs(fragment.duration - 8000) < 1

        cut_path = os.path.join(os.getcwd(), 'test', 'cut.wav')

        EditorInside.save_fragment(fragment, cut_path)

        assert (fragment.duration - get_wav_duration(cut_path)) < 1


