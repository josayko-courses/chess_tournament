"""Handle players information

"""

from controllers import TinyDB
from models import Player
from views import error_msg


class PlayerManager:
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
        rank = input("Rank ? [1 ~ 99+] ")
        try:
            rank = int(rank)
        except ValueError:
            error_msg("invalid input")
            return

        # Add to db
        id = self.table_players.insert(
            {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank}
        )

        p = Player(id, surname, name, birthdate, gender, rank)
        Player.p_list.append(p)

        print("Player creation successful !")
        input("Press ENTER to continue...\n")

    def edit_players_score(self, db_tournament, l_tournament, players, result):
        # l_players: local storage
        # db_players: db storage

        # local data
        for p in l_tournament.players:
            if p[0].id == players[0][0]:
                l_p1 = p
            elif p[0].id == players[1][0]:
                l_p2 = p

        # database
        for p in db_tournament['players']:
            if p[0] == players[0][0]:
                db_p1 = p
            elif p[0] == players[1][0]:
                db_p2 = p

        if result == 0:
            l_p1[1] += 1
            db_p1[1] += 1
        elif result == 1:
            l_p2[1] += 1
            db_p2[1] += 1
        elif result == 2:
            l_p1[1] += 0.5
            l_p2[1] += 0.5
            db_p1[1] += 0.5
            db_p2[1] += 0.5
        elif result == 3:
            l_p1[1] -= 1
            db_p1[1] -= 1
        elif result == 4:
            l_p2[1] -= 1
            db_p2[1] -= 1
        elif result == 5:
            l_p1[1] -= 0.5
            l_p2[1] -= 0.5
            db_p1[1] -= 0.5
            db_p2[1] -= 0.5

        p_list = []
        for p in db_tournament['players']:
            if p[0] == players[0][0]:
                p_list.append(db_p1)
            elif p[0] == players[1][0]:
                p_list.append(db_p2)
            else:
                p_list.append(p)

        self.table_tournaments.update(
            {'players': p_list},
            doc_ids=[db_tournament.doc_id],
        )
