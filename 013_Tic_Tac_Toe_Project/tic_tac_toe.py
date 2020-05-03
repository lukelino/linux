#! /usr/bin/python3
"""Tic-Tac-Toe game with AI"""


class TicTacToe:
    COORD = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0), 4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}
    OPTIONS = ['_', 'X', 'O']
    BATTLEFIELD = [[''] * 3 for _ in range(3)]

    def __init__(self):
        self.status = True
        self.battlefield = TicTacToe.BATTLEFIELD
        self.x = 0
        self.o = 0
        self.empty = 0

    def print_battlefield(self):
        print('-' * 9)
        for ele in self.battlefield:
            print('|', *ele, '|', sep=' ')
        print('-' * 9)

    def check_status(self):
        return self.status

    def start(self, user_input):
        if self.check_user_input_length(user_input):
            for i in range(9):
                if user_input[i] in TicTacToe.OPTIONS:
                    (x, y) = TicTacToe.COORD.get(i)
                    if user_input[i] == '_':
                        self.battlefield[x][y] = ' '
                    else:
                        self.battlefield[x][y] = user_input[i]
            self.count_x_y_empty(user_input)
            self.print_battlefield()
            self.next_to_play()
        else:
            print('Input too short')

    def count_x_y_empty(self, user_input):
        self.x = user_input.count('X')
        self.o = user_input.count('O')
        self.empty = user_input.count('_')

    def check_if_empty_field(self, crd):
        return self.battlefield[crd[0]][crd[1]] == ' '

    @staticmethod
    def check_user_input_length(user_input):
        return len(user_input) == 9

    @staticmethod
    def correct_range_coordinates(coordinates):
        return 1 <= coordinates < 4


    def next_to_play(self):

        coordinates = input('Enter the coordinates: ').split()

        if self.correct_range_coordinates(coordinates):
            if self.check_if_empty_field(coordinates):
                pass
        print('You should enter numbers!')




def main():
    tic_tac = TicTacToe()
    while tic_tac.check_status():
        tic_tac.start(input('Enter cells: '))


if __name__ == '__main__':
    main()
