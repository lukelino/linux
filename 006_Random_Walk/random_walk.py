#! /usr/local/bin/python3
""" Random walk """

import walk_class
import matplotlib.pyplot as plt


def main():
    rw = walk_class.RandomWalk()
    rw.fill_walk()

    plt.scatter(rw.x_values, rw.y_values, s=15)
    plt.show()


if __name__ == '__main__':
    main()