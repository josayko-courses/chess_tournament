"""Tournament related functionnalities

"""
from models import Tournament, Player


class TournamentManager:
    @staticmethod
    def create_tournament():
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

        # End date
        end = input("Length ? (days, default=1) ")
        try:
            end = int(end)
        except:
            end = 1

        # Description
        desc = input("Description ? ")

        t = Tournament(name, location, ratings[option], end, desc)
        Tournament.t_list.append(t)

        print(f"Tournament creation successful !")
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
            for i, t in enumerate(Tournament.t_list):
                print(f'    [ {i} ] {t.name}, {t.location}, {t.rating} === ', end="")
                nb = len(Tournament.t_list[i].players)
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

            if len(t.players) >= 8:
                cls.print_error("This tournament is full")
                return

            print("\n<< Registered players >>")
            t.print_players()
            print(f"Choose player to add to {t.name}, {t.location}: ")
            while True:
                for i, p in enumerate(Player.p_list):
                    print(f'    [ {i} ] {p.surname}, {p.name}, {p.rank}')
                select = input("Player ? ")
                try:
                    select = int(select)
                    if select < 0 or select >= len(Player.p_list):
                        continue
                    break
                except ValueError:
                    continue

            if any(player for player in t.players if player is Player.p_list[select]):
                cls.print_error("Player already registered in this tournament")
                return
            t.players.append(Player.p_list[select])

            print("Player registration successful !")
            input("Press ENTER to continue...\n")
