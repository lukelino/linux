class TicTacToe:
    COORD = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2)
    }
    PLAYER_COORD = {
        '11': (2, 0), '21': (2, 1), '31': (2, 2),
        '12': (1, 0), '22': (1, 1), '32': (1, 2),
        '13': (0, 0), '23': (0, 1), '33': (0, 2)
    }
    SIGNS = {'X': 1, 'O': 0}
    OPTIONS = ['_', 'X', 'O']
    BATTLEFIELD = [[''] * 3 for _ in range(3)]

    def __init__(self):
        self.status = True
        self.battlefield = TicTacToe.BATTLEFIELD
        self.x = 0
        self.o = 0
        self.empty = 0
        self.turn = 'X'
        self.winner = ''

    def print_battlefield(self):
        print('-' * 9)
        for i in range(3):
            print('| ', end='')
            for j in range(3):
                print(self.battlefield[i][j], end=' ')
            print('|')
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
            self.next_move()
        else:
            print('Input too short')

    def count_x_y_empty(self, user_input):
        self.x = user_input.count('X')
        self.o = user_input.count('O')
        self.empty = user_input.count('_')

    def check_if_empty_field(self, coord):
        tmp_coord = ''.join(coord)
        x, y = TicTacToe.PLAYER_COORD.get(f'{tmp_coord}')
        if self.battlefield[x][y] != ' ':
            print('This cell is occupied! Choose another one!')
            return False
        return True

    @staticmethod
    def check_user_input_length(user_input):
        return len(user_input) == 9

    # @staticmethod
    def correct_coordinates(self, crd):
        try:
            x, y = int(crd[0]), int(crd[1])
            if x < 1 or x > 3 or y < 1 or y > 3:
                print('Coordinates should be from 1 to 3!')
                return False
            elif ''.join(crd) not in TicTacToe.PLAYER_COORD:
                return False
            elif not self.check_if_empty_field(crd):
                return False
            return True
        except ValueError:
            print('You should enter numbers!')
            return False

    def check_turn(self):
        if self.x == self.o:
            self.x += 1
            return 'X'
        elif self.x > self.o:
            self.o += 1
            return 'O'
        self.x += 1
        return 'X'

    def next_move(self):
        """Next turn with 'X' or 'O' depending on the 'turn' status"""
        while self.empty:
            coord = input('Enter the coordinates: ').split()
            while not self.correct_coordinates(coord):
                coord = input('Enter the coordinates: ').split()
            tmp_coord = ''.join(coord)
            x, y = TicTacToe.PLAYER_COORD.get(f'{tmp_coord}')
            self.turn = self.check_turn()
            self.battlefield[x][y] = TicTacToe.SIGNS[f'{self.turn}']
            self.print_battlefield()
            self.empty -= 1
        self.check_result()

    def check_result(self):

        if self.empty > 0:
            print('Game not finished')
            self.status = True

        self.status = False
        print('THE END')


def main():
    tic_tac = TicTacToe()
    while tic_tac.check_status():
        tic_tac.start(input('Enter cells: '))


if __name__ == '__main__':
    main()