"""Handle players information

"""

from controllers import TinyDB
from models import Player
from views import error_msg


class PlayerManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.table = self.db.table('players')

    def create_player(self):
        """Get user input, create a new player and add it to the list"""

        print("+ Create player +")
        surname = input("Surname ? ")
        name = input("Name ? ")
        birthdate = input("Birth Date ? ")
        gender = input("Gender ? ")
        rank = input("Rank ? [1 ~ 99+] ")
        try:
            rank = int(rank)
        except ValueError:
            error_msg("invalid input")
            return

        # Add to db
        id = self.table.insert(
            {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank}
        )

        p = Player(id, surname, name, birthdate, gender, rank)
        Player.p_list.append(p)

        print("Player creation successful !")
        input("Press ENTER to continue...\n")

    def edit_player_score(self, tournament, id):
        players = tournament['players']
        for p in players:
            if p[0] == id:
                print(p)
        # Edit players total scores
        input("Press ENTER to continue...\n")
