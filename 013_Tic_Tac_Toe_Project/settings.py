class Settings:
    """Main game settings.py"""
    OPTIONS = ['user', 'easy', 'medium', 'hard']

    def __init__(self):
        self.battlefield = [[' '] * 3 for _ in range(3)]
        self.battlefield_size = 3 * 3
        self.status = True
        self.x = 0
        self.o = 0
        self.empty = 3 * 3
        self.turn = 'X'
        self.level = ''
        self.ai_choice_lst = list(range(9))
        self.player = ''

    def __repr__(self):
        print(self.battlefield, self.status, self.x, self.o, self.turn, self.level, self.player)

    def reset_settings(self):
        self.battlefield = [[' '] * 3 for _ in range(3)]
        self.battlefield_size = 3 * 3
        self.status = True
        self.x = 0
        self.o = 0
        self.empty = 3 * 3
        self.turn = 'X'
        self.level = ''
        self.ai_choice_lst = list(range(9))
        self.player = ''
