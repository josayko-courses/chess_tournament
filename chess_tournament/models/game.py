"""Game information

"""


class Game:
    """Create a game between two players (black and white) and holds the result.

    Result is initialize to "tbd" => To Be Determined
    """

    results = ("black", "draw", "white", "tbd")

    def __init__(self, black, white, result=results[3]):
        self.black = black
        self.white = white
        self.result = result

    def __repr__(self):
        b = f"{self.black.surname} {self.black.name} <black, rank: {self.black.rank}>"
        w = f"{self.white.surname} {self.white.name} <white, rank: {self.white.rank}>"
        return f"[ Result: {self.result} ] {b} vs. {w}"
