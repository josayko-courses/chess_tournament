"""Player information

"""


class Player:

    p_list = []

    def __init__(self, surname, name, birthdate, gender, rank):
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def __repr__(self):
        return f'<Player: {self.surname}, {self.name}, {self.birthdate}, {self.gender}, {self.rank}>'
