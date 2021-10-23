"""Player information

"""


class Player:
    def __init__(self, id, surname, name, birthdate, gender, rank):
        self.id = id
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def deserialize(p):
        inst = Player(p.doc_id, p['surname'], p['name'], p['birthdate'], p['gender'], p['rank'])
        return inst

    def __repr__(self):
        return f"Player(id={self.id}, surname={self.surname}, name={self.name}, birthdate={self.birthdate}, gender={self.gender}, rank={self.rank})"
