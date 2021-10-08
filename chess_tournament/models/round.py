"""Round information

"""

from datetime import datetime, timedelta


class Round:
    def __init__(self, name, games):
        self.name = name
        self.start = datetime.today().strftime('%Y-%m-%d %H:%M')
        self.end = ""
        self.games = games
        return

    def __repr__(self):
        return f"<{self.name}, {self.start}, {self.end}, {self.games}>"
