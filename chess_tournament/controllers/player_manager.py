"""Handle players information

"""

from controllers import TinyDB
from models import Player
from views import error_msg, show_players


class PlayerManager:
    """Handle player creation and rank update"""

    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.table_players = self.db.table('players')
        self.table_tournaments = self.db.table('tournaments')

    def create_player(self):
        """Get user input, create a new player and add it to the list"""

        print("+ Create player +")
        surname = input("Surname ? ")
        name = input("Name ? ")
        birthdate = input("Birth Date ? ")
        gender = input("Gender ? ")
        rank = input("Rank ? ")
        try:
            rank = int(rank)
        except ValueError:
            return error_msg("invalid input")

        # Add to db
        id = self.table_players.insert(
            {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank}
        )
        p = Player(id, surname, name, birthdate, gender, rank)
        Player.p_list.append(p)
        print("Player creation successful !")
        input("Press ENTER to continue...\n")

    def edit_player_rank(self):
        """Edit player rank"""

        print("+ Edit player rank +")
        id_list = [x.id for x in Player.p_list]
        show_players(Player.p_list)

        id = input("Select player id: ")
        try:
            id = int(id)
            if id not in id_list:
                return error_msg("invalid id")
        except ValueError:
            ("ERROR")
            return error_msg("invalid input")

        for p in Player.p_list:
            new_rank = ""
            if p.id == id:
                print(f"    /* Edit {p.surname} {p.name}, rank: {p.rank} */")
                old_rank = p.rank
                new_rank = input("New rank ? ")
                break
        try:
            new_rank = int(new_rank)
            p.rank = new_rank
            print(f"    {p.surname} {p.name}, rank: {old_rank} => rank: {new_rank}")
        except ValueError:
            return error_msg("invalid input")
        self.table_players.update({'rank': new_rank}, doc_ids=[id])
        input("Press ENTER to continue...")
