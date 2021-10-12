"""Tournament information

"""
from datetime import datetime, timedelta


class Tournament:
    """Holds the information of the tournament"""

    t_list = []

    def __init__(self, id, name, location, rating, start, end, desc):
        self.id = id
        self.name = name
        self.location = location
        self.start = start
        if end:
            self.end = end
        else:
            self.end = self.start
        self.nb_rounds = 4
        self.rounds = []
        self.players = []
        self.rating = rating
        self.desc = desc

    def __repr__(self):
        return f"<{self.name}, {self.location}, {self.rating}, {self.start}, {self.end}>"

    def print_players(self):
        if len(self.players) == 0:
            print("*** This tournament is empty ***")
        else:
            for p in self.players:
                print(
                    f"id: {p[0].id}, name: {p[0].surname} {p[0].name}, birthdate: {p[0].birthdate}, gender: {p[0].gender}, rank: {p[0].rank}"
                )
