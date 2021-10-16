"""Round information

"""

from datetime import datetime


class Round:
    """Holds round information"""

    def __init__(self, name, games, start=None, end=None):
        self.name = name
        if start == None:
            self.start = datetime.today().strftime('%Y-%m-%d %H:%M')
        else:
            self.start = start
        if end == None:
            self.end = ""
        else:
            self.end = end
        self.games = games

    def __repr__(self):
        return f"<{self.name}, {self.start}, {self.end}, {self.games}>"
