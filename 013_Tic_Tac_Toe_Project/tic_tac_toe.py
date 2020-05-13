""""Tic Tac Toe with AI"""
import settings
import game_functions as gf


def main():
    g_settings = settings.Settings()
    while True:
        user_cmd = input('Input command: ').split()
        if user_cmd[0] == 'exit':
            break
        elif len(user_cmd) == 3 and user_cmd[0] == 'start' and user_cmd[1] in g_settings.OPTIONS\
                and user_cmd[2] in g_settings.OPTIONS:
            gf.print_battlefield(g_settings)
            gf.start_game(g_settings, user_cmd)
            if not gf.check_status(g_settings):
                g_settings.reset_settings()
                # g_settings.__repr__()
        else:
            print('Bad parameters!')


if __name__ == '__main__':
    main()
