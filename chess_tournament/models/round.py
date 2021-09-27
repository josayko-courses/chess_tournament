"""Round information

"""

from .game import Game


class Round:
    def __init__(self):
        # Create games
        self.games = []
        return

    def create_game(self, black, white):
        new_game = Game(black, white)
        self.games.append(new_game)
