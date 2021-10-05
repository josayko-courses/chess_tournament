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
        if len(name) < 2:
            print("*** Error: input must be more than 1 character ***")
            input("Press ENTER to cancel...\n")
            return

        location = input("Location ? ")
        if len(location) < 2:
            print("*** Error: input must be more than 1 character ***")
            input("Press ENTER to cancel...\n")
            return

        # Rating choice. Loop until user enter a valid option
        while True:
            rating = input("Rating type :\n    1 rapid\n    2 blitz\n    3 bullet\n    Rating ? (1 - 3) ")
            try:
                rating = int(rating)
                if rating > 0 and rating <= 3:
                    option = int(option) - 1
                    break
            except ValueError:
                print("*** Error: invalid input ***")
                input("Press ENTER to cancel...\n")
                return

        # Start date
        start = input("Start date ? ")

        # End date
        end = input("End date ? ")

        # Description
        desc = input("Description ? ")

        # Add to db
        id = self.table.insert(
            {
                'name': name,
                'location': location,
                'rating': ratings[option],
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

    def print_error(self, str):
        print(f"*** {str} ***")
        input("Press ENTER to cancel...\n")

    def add_player(self):
        """Add players to tournament"""

        print("+ Add player to tournament +")
        if not Tournament.t_list:
            self.print_error("No tournament available")
        elif not Player.p_list:
            self.print_error("No players available")
        else:
            tour_lst = [tour for tour in Tournament.t_list]
            if len(tour_lst) == 0:
                self.print_error("No tournament available")
                return
            for i, t in enumerate(tour_lst):
                print(f'    [ {i + 1} ] {t.name}, {t.location}, {t.rating} === ', end="")
                nb = len(tour_lst[i].players)
                print(f'{nb}/8 Players')
            select = input("Select tournament: ")
            try:
                select = int(select) - 1
                if select < 0 or select >= len(Tournament.t_list):
                    self.print_error("Error: invalid input")
                    return
            except ValueError:
                self.print_error("Error: invalid input")
                return

            if len(Tournament.t_list[select].players) >= 8:
                self.print_error("This tournament is full")
                return

            print("\n<< Registered players >>")
            Tournament.t_list[select].print_players()
            print()
            print(f"Choose player to add to {Tournament.t_list[select].name}, {Tournament.t_list[select].location}: ")
            while True:
                players_id = [p[0].id for p in Tournament.t_list[select].players]
                player_lst = [player for player in Player.p_list if player.id not in players_id]
                if len(player_lst) == 0:
                    self.print_error("Not enough players")
                    return

                for i, p in enumerate(player_lst):
                    print(f'    [ {i + 1} ] {p.surname}, {p.name}, {p.rank}')
                p_select = input("Player ? ")
                try:
                    p_select = int(p_select) - 1
                    if p_select < 0 or p_select >= len(player_lst):
                        continue
                    break
                except ValueError:
                    continue

            Tournament.t_list[select].players.append((player_lst[p_select], 0))

            tournament = self.table.get(doc_id=Tournament.t_list[select].id)
            p_list = tournament['players']
            p_list.append((player_lst[p_select].id, 0))
            self.table.update(
                {'players': p_list},
                doc_ids=[Tournament.t_list[select].id],
            )

            print("Player registration successful !")
            input("Press ENTER to continue...\n")
