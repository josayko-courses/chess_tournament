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

        # Update game on db
        db = Database(dirname)
        for t in db.tournaments:
            if t.doc_id == tournament_id:
                break

        updated_games = []
        for i, g in enumerate(t['rounds'][-1]['games']):
            if i == game_index:
                updated_games.append(game)
            else:
                updated_games.append(g)

        updated_rounds = []
        print("game_index: ", game_index)
        for i, r in enumerate(t['rounds']):
            if i == len(t['rounds']) - 1:
                serialized_round = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'games': updated_games}
                updated_rounds.append(serialized_round)
            else:
                updated_rounds.append(r)

        db.tournaments.update(
            {'rounds': updated_rounds},
            doc_ids=[tournament_id],
        )

        # Update total scores on db
        return
