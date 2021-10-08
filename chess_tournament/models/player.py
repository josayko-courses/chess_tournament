"""Player information

"""


class Player:

    p_list = []

    def __init__(self, id, surname, name, birthdate, gender, rank):
        self.id = id
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def __repr__(self):
        return f'<id: {self.id}, {self.surname}, {self.name}, {self.birthdate}, {self.gender}, rank: {self.rank}>'
