"""Program initialization and local data

"""

from models import Tournament, Player, Database


class App:

    tournaments = []
    players = []

    @classmethod
    def program_initialization(cls, dirname):
        db = Database(dirname)
        cls.load_data_from_db(db.players, Player, cls.players)
        cls.load_data_from_db(db.tournaments, Tournament, cls.tournaments)
        return

    @staticmethod
    def load_data_from_db(table, model, app_data):
        for el in table.all():
            inst = model.deserialize(el)
            app_data.append(inst)
