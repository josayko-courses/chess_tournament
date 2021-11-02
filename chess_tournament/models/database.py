"""Database tables

"""

from tinydb import TinyDB


class Database:
    def __init__(self, dirname):
        db = TinyDB(dirname + '/db.json')
        self.players = db.table('players')
        self.tournaments = db.table('tournaments')

    def add_round_to_tournament(self, round, tournament_id):
        for t in self.tournaments:
            if t.doc_id == tournament_id:
                t['rounds'].append(round)
                self.tournaments.update(t, doc_ids=[tournament_id])

    def update_results(self, tournament, game, game_index, player1, player2):
        for t in self.tournaments:
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
        self.tournaments.update(
            {'rounds': updated_rounds, 'players': updated_players},
            doc_ids=[tournament.id],
        )
        return

    def set_round_end(self, tournament):
        for t in self.tournaments:
            if t.doc_id == tournament.id:
                t['rounds'][-1]['end'] = tournament.rounds[-1].end
                self.tournaments.update(t, doc_ids=[tournament.id])

        return
