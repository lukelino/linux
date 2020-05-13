import random


class Hard:

    @staticmethod
    def ai_move(g_settings):
        ai_x = random.randint(0, 2)
        ai_y = random.randint(0, 2)
        while g_settings.battlefield[ai_x][ai_y] != ' ':
            ai_x = random.randint(0, 2)
            ai_y = random.randint(0, 2)
        print('HARD')
        g_settings.player = 'human'
        return ai_x, ai_y
