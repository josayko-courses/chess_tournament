"""Player information

"""

from tinydb import TinyDB


class Player:
    def __init__(self, id, surname, name, birthdate, gender, rank):
        self.id = id
        self.surname = surname
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank

    def deserialize(p):
        """From data in db create new player instance"""
        inst = Player(p.doc_id, p['surname'], p['name'], p['birthdate'], p['gender'], p['rank'])
        return inst

    def __repr__(self):
        str1 = f"Player(id={self.id}, surname={self.surname}, name={self.name}, "
        str2 = f"birthdate={self.birthdate}, gender={self.gender}, rank={self.rank})"
        return str1 + str2

    def save_player_to_db(self, dirname):
        """Save player to db"""
        db = TinyDB(dirname + '/db.json')
        players_table = db.table('players')
        new_player = {
            'surname': self.surname,
            'name': self.name,
            'birthdate': self.birthdate,
            'gender': self.gender,
            'rank': self.rank,
        }
        return players_table.insert(new_player)

    def update_player_to_db(self, new_rank, dirname):
        """Update player rank to db"""
        db = TinyDB(dirname + '/db.json')
        players_table = db.table('players')
        players_table.update({'rank': new_rank}, doc_ids=[self.id])
