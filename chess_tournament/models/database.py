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
