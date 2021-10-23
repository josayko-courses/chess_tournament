"""Tournament information

"""


class Tournament:
    def __init__(self, id, name, location, rating, desc, start, end=None):
        self.id = id
        self.name = name
        self.location = location
        self.rating = rating

        self.nb_rounds = 4
        self.rounds = []
        self.players = []

        self.start = start
        if end == None:
            self.end = start
        else:
            self.end = end

        self.desc = desc

    def deserialize(t):
        inst = Tournament(t.doc_id, t['name'], t['location'], t['rating'], t['desc'], t['start'], t['end'])
        inst.players = t['players']
        return inst

    def serialize(t, table):
        data = []
        return data

    def __repr__(self) -> str:
        str1 = f"Tournament(id={self.id}, name={self.name}, location={self.location}, rating={self.rating}, "
        str2 = f"desc={self.desc}, start={self.start}, end={self.end})"
        return str1 + str2
