import easy


class Medium(easy.Easy):

    @staticmethod
    def possible_moves(g_settings):
        tmp_lst = list(zip(*g_settings.battlefield))
        diag_lst_1 = [g_settings.battlefield[i][i] for i in range(3)]
        diag_lst_2 = [g_settings.battlefield[2 - i][i] for i in range(3)]

        g_settings.player = 'human'

        if g_settings.turn == 'X':
            if diag_lst_1.count('X') == 2 and diag_lst_1.count(' ') == 1:
                return diag_lst_1.index(' '), diag_lst_1.index(' ')
            if diag_lst_2.count('X') == 2 and diag_lst_2.count(' ') == 1:
                x = diag_lst_1.index(' ')
                return 2 - x, x
            for i in range(3):
                if g_settings.battlefield[i].count('X') == 2 and g_settings.battlefield[i].count(' ') == 1:
                    return i, g_settings.battlefield[i].index(' ')
                if tmp_lst[i].count('X') == 2 and tmp_lst[i].count(' ') == 1:
                    return tmp_lst[i].index(' '), i

            x, y = easy.Easy.ai_move(g_settings)
            return x, y

        elif g_settings.turn == 'O':
            if diag_lst_1.count('O') == 2 and diag_lst_1.count(' ') == 1:
                return diag_lst_1.index(' '), diag_lst_1.index(' ')
            if diag_lst_2.count('O') == 2 and diag_lst_2.count(' ') == 1:
                x = diag_lst_1.index(' ')
                return 2 - x, x
            for i in range(3):
                if g_settings.battlefield[i].count('O') == 2 and g_settings.battlefield[i].count(' ') == 1:
                    return i, g_settings.battlefield[i].index(' ')
                if tmp_lst[i].count('O') == 2 and tmp_lst[i].count(' ') == 1:
                    return tmp_lst[i].index(' '), i

            x, y = easy.Easy.ai_move(g_settings)
            return x, y
