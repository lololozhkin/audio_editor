import os
import time
from yadisk import YaDisk
import yadisk


def get_path(name, chan):
    return os.path.join(os.getcwd(), "samples", chan, name)


def in_pieces(name, chan):
    return os.path.join(os.getcwd(), "samples", chan, "pieces", name)


def main():
    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples")}')
    except Exception as e:
        print('samples')

    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples", "mono")}')
    except Exception as e:
        print('mono')

    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples", "stereo")}')
    except Exception as e:
        print('stereo')

    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples", "stereo", "pieces")}')
    except Exception as e:
        print('stereo/pieces')

    try:
        os.mkdir(f'{os.path.join(os.getcwd(), "samples", "mono", "pieces")}')
    except Exception as e:
        print('mono/pieces')

    FILES = {
        'https://yadi.sk/d/wMu8iINSR2m3pA': get_path('result.mp3',
                                                     'stereo'),
        'https://yadi.sk/d/VhTIu8gUJUGHmQ': get_path('full_speach.mp3',
                                                     'stereo'),
        'https://yadi.sk/d/hGmP6J5uQE0EQg': in_pieces('luschshe.wav',
                                                      'stereo'),
        'https://yadi.sk/d/eqqpNhkq_ToFmg': in_pieces('on.wav',
                                                      'stereo'),
        'https://yadi.sk/d/aebXgp8fQ323Ug': in_pieces('pit.wav',
                                                      'stereo'),
        'https://yadi.sk/d/EvoOaCJ8JjciAg': in_pieces('speach_only.wav',
                                                      'stereo'),
        'https://yadi.sk/d/pFePvfrhunzOoA': in_pieces('zhizni_grazhdan.wav',
                                                      'stereo'),

        'https://yadi.sk/d/KngUlqTo9CYGRw': get_path('result.wav',
                                                     'mono'),
        'https://yadi.sk/d/XRLjLm83TlOe1w': get_path('full_speach.mp3',
                                                     'mono'),
        'https://yadi.sk/d/gUiVzsvuT5BDnQ': in_pieces('luschshe.wav',
                                                      'mono'),
        'https://yadi.sk/d/yzGmTTLZ6DV3dA': in_pieces('on.wav',
                                                      'mono'),
        'https://yadi.sk/d/4T3Bv2hPwKl7bA': in_pieces('pit.wav',
                                                      'mono'),
        'https://yadi.sk/d/-dqYs3UDbgVc1g': in_pieces('speach_only.wav',
                                                      'mono'),
        'https://yadi.sk/d/nMiHKbmlM0r9iQ': in_pieces('zhizni_grazhdan.wav',
                                                      'mono')
    }

    pwd = os.getcwd()
    y = YaDisk()
    while True:
        try:
            for pair in FILES.items():
                y.download_public(pair[0], pair[1])
                time.sleep(2)
            break
        except yadisk.exceptions.TooManyRequestsError as e:
            pass


if __name__ == '__main__':
    main()
