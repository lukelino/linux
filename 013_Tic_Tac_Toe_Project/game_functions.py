import easy
import medium
import hard
import player


def print_battlefield(g_settings):
    print('-' * g_settings.battlefield_size)
    for i in range(3):
        print('| ', end='')
        for j in range(3):
            print(g_settings.battlefield[i][j], end=' ')
        print('|')
    print('-' * g_settings.battlefield_size)


def start_game(g_settings, cmd):
    x, y = 0, 0
    if cmd[1] == 'user' and cmd[2] == 'user':
        g_settings.level = ''
        x, y = player.Player.player_move(g_settings)
        g_settings.player = g_settings.level
        execute_job(g_settings, x, y)
    elif cmd[1] != 'user' and cmd[2] == 'user':
        g_settings.level = cmd[1]
        if g_settings.level == 'easy':
            x, y = easy.Easy.ai_move(g_settings)
        elif g_settings.level == 'medium':
            x, y = medium.Medium.ai_move(g_settings)
        elif g_settings.level == 'hard':
            x, y = hard.Hard.ai_move(g_settings)
        execute_job(g_settings, x, y)
    elif cmd[1] != 'user' and cmd[2] != 'user':
        g_settings.level = cmd[1]
        x, y = player.Player.player_move(g_settings)
        execute_job(g_settings, x, y)
    elif cmd[1] == 'user' and cmd[2] != 'user':
        g_settings.level = cmd[2]
        x, y = player.Player.player_move(g_settings)
        g_settings.player = g_settings.level
        execute_job(g_settings, x, y)


def check_turn(g_settings):
    if g_settings.x == g_settings.o:
        g_settings.x += 1
        return 'X'
    elif g_settings.x > g_settings.o:
        g_settings.o += 1
        return 'O'
    g_settings.x += 1
    return 'X'


def next_to_move(g_settings):
    while g_settings.empty and g_settings.status:
        if g_settings.player == 'human' and g_settings.status:
            x, y = player.Player.player_move(g_settings)
            execute_job(g_settings, x, y)
        elif g_settings.player == 'easy' and g_settings.status:
            x, y = easy.Easy.ai_move(g_settings)
            execute_job(g_settings, x, y)
        elif g_settings.player == 'medium' and g_settings.status:
            x, y = medium.Medium.possible_moves(g_settings)
            execute_job(g_settings, x, y)
        elif g_settings.player == 'hard' and g_settings.status:
            x, y = hard.Hard.ai_move(g_settings)
            execute_job(g_settings, x, y)


def execute_job(g_settings, x, y):
    g_settings.turn = check_turn(g_settings)
    g_settings.battlefield[x][y] = g_settings.turn
    print_battlefield(g_settings)
    g_settings.empty -= 1
    check_result(g_settings)
    if check_status(g_settings):
        next_to_move(g_settings)


def check_status(g_settings):
    return g_settings.status


def check_result(g_settings):
    tmp_lst = list(zip(*g_settings.battlefield))
    if any([all([x == 'X' for x in g_settings.battlefield[i]]) for i in range(3)]) \
            or any([all([x == 'X' for x in tmp_lst[i]]) for i in range(3)]):
        print('X wins')
        g_settings.status = False
    elif any([all([x == 'O' for x in g_settings.battlefield[i]]) for i in range(3)]) \
            or any([all([x == 'O' for x in tmp_lst[i]]) for i in range(3)]):
        print('O wins')
        g_settings.status = False
    elif all([x == 'X' for x in [g_settings.battlefield[i][i] for i in range(3)]]) \
            or all([x == 'X' for x in [g_settings.battlefield[2 - i][i] for i in range(3)]]):
        print('X wins')
        g_settings.status = False
    elif all([x == 'O' for x in [g_settings.battlefield[i][i] for i in range(3)]]) \
            or all([x == 'O' for x in [g_settings.battlefield[2 - i][i] for i in range(3)]]):
        print('O wins')
        g_settings.status = False
    elif g_settings.empty == 0:
        print('Draw')
        g_settings.status = False
    elif g_settings.status and g_settings.empty > 0 and g_settings.level:
        print(f"""Making move level "{g_settings.level}\"""")
        g_settings.status = True
