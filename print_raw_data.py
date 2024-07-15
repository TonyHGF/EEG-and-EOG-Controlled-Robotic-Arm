from pyOpenBCI import OpenBCICyton
import numpy as np

def print_raw(sample):
    # print(str(sample))
    print(sample.__dict__)
    # exit()


def main():

    board = OpenBCICyton(port='COM5', daisy=False)
    board.start_stream(print_raw)
    board.stop_stream()

if __name__ == '__main__':
    main()


