class Player:

    @staticmethod
    def player_move(g_settings):
        coord = input('Enter the coordinates: ').split()
        while not Player.correct_coordinates(g_settings, coord):
            coord = input('Enter the coordinates: ').split()
        x = 3 - int(coord[1])
        y = int(coord[0]) - 1
        if g_settings.level == '':
            g_settings.player = 'human'
        else:
            g_settings.player = g_settings.level
        return x, y

    @staticmethod
    def correct_coordinates(g_settings, coord):
        try:
            x = 3 - int(coord[1])
            y = int(coord[0]) - 1
            print(f'x: {3 - int(coord[1])}, y: {int(coord[0]) - 1}')
            if x < 0 or x > 3 or y < 0 or y > 3:
                print('Coordinates should be from 1 to 3!')
                return False
            elif not g_settings.battlefield[x][y] == ' ':
                print('This cell is occupied! Choose another one!')
                return False
            return True
        except ValueError:
            print('You should enter numbers!')
            return False
