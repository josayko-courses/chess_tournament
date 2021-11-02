"""Program initialization and local data

"""

from models import Tournament, Player
from tinydb import TinyDB


class App:

    tournaments = []
    players = []

    @classmethod
    def program_initialization(cls, dirname):
        """Initialize program database or create new database if not found"""
        db = TinyDB(dirname + '/db.json')
        players_table = db.table('players')
        tournaments_table = db.table('tournaments')
        cls.load_data_from_db(players_table, Player, cls.players)
        cls.load_data_from_db(tournaments_table, Tournament, cls.tournaments)
        return

    @staticmethod
    def load_data_from_db(table, model, app_data):
        """Load data from db"""
        for el in table.all():
            inst = model.deserialize(el)
            app_data.append(inst)
