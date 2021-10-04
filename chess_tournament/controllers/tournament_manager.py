"""Tournament related functionnalities

"""

from controllers import TinyDB, Query
from models import Tournament, Player


class TournamentManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(self.db_path)
        self.table = self.db.table('tournaments')

    def create_tournament(self):
        """Get user input, create a new tournament and add it to the list"""

        print("+ Create tournament +")
        # Rating choices, default is 'rapid'
        ratings = ('rapid', 'blitz', 'bullet')
        option = 0

        # Tournament name and location
        name = input("Name ? ")
        location = input("Location ? ")

        # Rating choice. Loop until user enter a valid option
        while True:
            rating = input("Rating type :\n    1 rapid\n    2 blitz\n    3 bullet\n    Rating ? (1 - 3) ")
            try:
                rating = int(rating)
                if rating > 0 and rating <= 3:
                    option = int(option) - 1
                    break
            except ValueError:
                continue

        # Start date
        start = input("Start date ? (days, default=1) ")
        try:
            start = int(start)
        except ValueError:
            start = 1

        # End date
        end = input("End date ? (days, default=1) ")
        try:
            end = int(end)
        except ValueError:
            end = 1

        # Description
        desc = input("Description ? ")

        # Add to db
        id = self.table.insert(
            {
                'name': name,
                'location': location,
                'rating': rating,
                'nb_rounds': 4,
                'rounds': [],
                'players': [],
                'start': start,
                'end': end,
                'desc': desc,
            }
        )

        # Add to local data
        t = Tournament(id, name, location, ratings[option], start, end, desc)
        Tournament.t_list.append(t)

        print("Tournament creation successful !")
        input("Press ENTER to continue...\n")

    def print_error(str):
        print(f"*** {str} ***")
        input("Press ENTER to cancel...\n")

    @classmethod
    def add_player(cls):
        """Add players to tournament"""

        print("+ Add player to tournament +")
        if not Tournament.t_list:
            cls.print_error("No tournament available")
        elif not Player.p_list:
            cls.print_error("No players available")
        else:
            tour_lst = [tour for tour in Tournament.t_list if len(tour.players) < 8]
            if len(tour_lst) == 0:
                cls.print_error("No tournament available")
                return
            for i, t in enumerate(tour_lst):
                print(f'    [ {i} ] {t.name}, {t.location}, {t.rating} === ', end="")
                nb = len(tour_lst[i].players)
                print(f'{nb}/8 Players')
            select = input("Select tournament: ")
            try:
                select = int(select)
                if select < 0 or select >= len(Tournament.t_list):
                    cls.print_error("Error: invalid input")
                    return
            except ValueError:
                cls.print_error("Error: invalid input")
                return

            if len(Tournament.t_list[select].players) >= 8:
                cls.print_error("This tournament is full")
                return

            print("\n<< Registered players >>")
            Tournament.t_list[select].print_players()
            print()
            print(f"Choose player to add to {t.name}, {t.location}: ")
            while True:
                player_lst = [player for player in Player.p_list if player not in Tournament.t_list[select].players]
                if len(player_lst) == 0:
                    cls.print_error("Not enough players")
                    return

                for i, p in enumerate(player_lst):
                    print(f'    [ {i} ] {p.surname}, {p.name}, {p.rank}')
                nb = input("Player ? ")
                try:
                    nb = int(nb)
                    if nb < 0 or nb >= len(player_lst):
                        continue
                    break
                except ValueError:
                    continue

            Tournament.t_list[select].players.append(player_lst[nb])

            print("Player registration successful !")
            input("Press ENTER to continue...\n")
