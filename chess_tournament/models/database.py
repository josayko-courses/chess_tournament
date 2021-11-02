"""Database tables

"""

from tinydb import TinyDB


class Database:
    def __init__(self, dirname):
        db = TinyDB(dirname + '/db.json')
        self.players = db.table('players')
        self.tournaments = db.table('tournaments')

    def set_round_end(self, tournament):
        for t in self.tournaments:
            if t.doc_id == tournament.id:
                t['rounds'][-1]['end'] = tournament.rounds[-1].end
                self.tournaments.update(t, doc_ids=[tournament.id])

        return
