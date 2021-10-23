"""Program initialization and local data

"""

from models import Tournament, Database


class App:

    tournaments = []
    players = []

    @classmethod
    def program_initialization(cls, dirname):
        db = Database(dirname)
        print(db.players)
        print(db.tournaments)
        return
