"""Round information

"""


class Round:
    def __init__(self):
        # Create games
        self.games = []
        return

    def create_game(self, p1, p2):
        self.games.append(([p1, 0], [p2, 0]))
