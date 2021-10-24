"""Round Manager

"""

from controllers import App


class RoundManager:
    def update_results(dirname, result, game):
        if result == 1:
            game[0][1] = 1
            game[1][1] = 0
        elif result == 2:
            game[0][1] = 0
            game[1][1] = 1
        elif result == 3:
            game[0][1] = 0.5
            game[1][1] = 0.5
        elif result == 4:
            game[0][1] = 0
            game[1][1] = 0
        return
