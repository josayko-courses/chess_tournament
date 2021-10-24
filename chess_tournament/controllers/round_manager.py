"""Round Manager

"""

from models import Database
from controllers import App


class RoundManager:
    def update_results(dirname, result, game, game_index, tournament_id):
        # Update game score locally
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

        # Update total scores locally
        print(App.tournaments[-1].players)

        # Update game on db
        db = Database(dirname)
        for t in db.tournaments:
            if t.doc_id == tournament_id:
                games_on_db = t['rounds'][-1]['games']
                break
        print(games_on_db)

        # Update total scores on db
        return
