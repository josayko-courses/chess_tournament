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
