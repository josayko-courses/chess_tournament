"""Tournament information

"""
from datetime import datetime, timedelta


class Tournament:
    """Holds the information of the tournament"""

    def __init__(self, name, location, rating, end):
        self.name = name
        self.location = location
        self.start = datetime.today().strftime('%Y-%m-%d')
        if end:
            td = timedelta(end - 1) if end - 1 > 0 else timedelta(0)
            self.end = (datetime.today() + td).strftime('%Y-%m-%d')
        else:
            self.end = self.start
        self.nb_rounds = 4
        self.rounds = []
        self.players = []
        self.rating = rating

    def __repr__(self):
        return f'{self.name}, {self.location}, {self.rating}, {self.start}, {self.end}'
