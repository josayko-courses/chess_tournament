"""Tournament information

"""
from datetime import datetime, timedelta


class Tournament:
    """Holds the information of the tournament"""

    def __init__(self, name, location, end=0):
        self.name = name
        self.location = location
        self.start = datetime.today().strftime('%Y-%m-%d')
        if end:
            td = timedelta(days=end)
            self.end = (datetime.today() + td).strftime('%Y-%m-%d')
        else:
            self.end = self.start
        self.nb_rounds = 4
        self.rounds = []
        self.players = []
