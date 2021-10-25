"""Database tables

"""

from tinydb import TinyDB


class Database:
    def __init__(self, dirname):
        db = TinyDB(dirname + '/db.json')
        self.players = db.table('players')
        self.tournaments = db.table('tournaments')

    def add_player_to_tournament(self, player, tournament_id):
        for t in self.tournaments:
            if t.doc_id == tournament_id:
                t['players'].append(player)
                self.tournaments.update(t, doc_ids=[tournament_id])

    def create_tournament(self, input):
        if not input['end']:
            input['end'] = input['start']

        new_tournament = {
            'name': input['name'],
            'location': input['location'],
            'rating': input['rating'],
            'nb_rounds': 4,
            'rounds': [],
            'players': [],
            'start': input['start'],
            'end': input['end'],
            'desc': input['desc'],
        }
        return self.tournaments.insert(new_tournament)

    def create_player(self, input):
        new_player = {
            'surname': input['surname'],
            'name': input['name'],
            'birthdate': input['birthdate'],
            'gender': input['gender'],
            'rank': input['rank'],
        }
        return self.players.insert(new_player)

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
