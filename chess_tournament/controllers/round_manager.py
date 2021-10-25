"""Round Manager

"""

from models import Database
from controllers import App


class RoundManager:
    def reset_game_results(game, player1, player2):
        """Reset game results to 0 for both players"""
        if game[0][1] == 1:
            player1[1] -= 1
        elif game[0][1] == 0.5:
            player1[1] -= 0.5
        if game[1][1] == 1:
            player2[1] -= 1
        elif game[1][1] == 0.5:
            player2[1] -= 0.5
        game[0][1] = 0
        game[1][1] = 0
        return

    def update_results(dirname, result, games, game_index, tournament):
        # Get players total score reference
        game = games[game_index]
        for p in tournament.players:
            if p[0] == game[0][0]:
                player1 = p
            if p[0] == game[1][0]:
                player2 = p

        # Update game score + individual score
        RoundManager.reset_game_results(game, player1, player2)
        if result == 1:
            player1[1] += 1
            game[0][1] = 1
            game[1][1] = 0
        elif result == 2:
            player2[1] += 1
            game[0][1] = 0
            game[1][1] = 1
        elif result == 3:
            player1[1] += 0.5
            player2[1] += 0.5
            game[0][1] = 0.5
            game[1][1] = 0.5

        # Update db
        db = Database(dirname)
        for t in db.tournaments:
            if t.doc_id == tournament.id:
                break

        # Edit game
        updated_games = []
        for i, g in enumerate(t['rounds'][-1]['games']):
            if i == game_index:
                updated_games.append(game)
            else:
                updated_games.append(g)

        # Edit round with updated game
        updated_rounds = []
        for i, r in enumerate(t['rounds']):
            if i == len(t['rounds']) - 1:
                serialized_round = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'games': updated_games}
                updated_rounds.append(serialized_round)
            else:
                updated_rounds.append(r)

        # Edit players total score
        updated_players = []
        for p in t['players']:
            if p[0] == player1[0]:
                updated_players.append(player1)
            elif p[0] == player2[0]:
                updated_players.append(player2)
            else:
                updated_players.append(p)

        # Save to db
        db.tournaments.update(
            {'rounds': updated_rounds, 'players': updated_players},
            doc_ids=[tournament.id],
        )
        return
