import os
import time
from yadisk import YaDisk


def get_path(name):
    return os.path.join(os.getcwd(), "samples", name)


def in_pieces(name):
    return os.path.join(os.getcwd(), "samples", "pieces", name)


def main():
    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples")}')
    except Exception as e:
        pass

    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples", "pieces")}')
    except Exception as e:
        pass

    FILES = {
        'https://yadi.sk/d/wMu8iINSR2m3pA': get_path('result.wav'),
        'https://yadi.sk/d/VhTIu8gUJUGHmQ': get_path('full_speach.mp3'),
        'https://yadi.sk/d/hGmP6J5uQE0EQg': in_pieces('luschshe.wav'),
        'https://yadi.sk/d/eqqpNhkq_ToFmg': in_pieces('on.wav'),
        'https://yadi.sk/d/aebXgp8fQ323Ug': in_pieces('pit.wav'),
        'https://yadi.sk/d/EvoOaCJ8JjciAg': in_pieces('speach_only.wav'),
        'https://yadi.sk/d/pFePvfrhunzOoA': in_pieces('zhizni_grazhdan.wav')
    }

    pwd = os.getcwd()
    y = YaDisk()
    for pair in FILES.items():
        y.download_public(pair[0], pair[1])
        time.sleep(1)


if __name__ == '__main__':
    main()
