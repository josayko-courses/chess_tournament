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
        end = input("Length ? (days) ")

        # Description
        desc = input("Description ? ")

        t = Tournament(name, location, ratings[option], int(end), desc)
        Tournament.t_list.append(t)

        print(f"New tournament created !")
        print(f">> Name: {t.name}")
        print(f">> Location: {t.location}")
        print(f">> Rating: {t.rating}")
        print(f">> From: {t.start}")
        print(f">> To: {t.end}")
        print(f">> Description: {t.desc}")
        print()

    @staticmethod
    def add_player():
        """Add players to tournament"""

        print("+ Add player to tournament +")
        if not Tournament.t_list:
            print("*** No tournament available ***")
            input("Press ENTER to cancel\n")
        else:
            while True:
                for i, t in enumerate(Tournament.t_list):
                    print(f'    [ {i} ] {t.name}, {t.location}, {t.rating} === ', end="")
                    nb = len(Tournament.t_list[i].players)
                    print(f'{nb}/8 Players')
                select = input("Select tournament: ")
                try:
                    select = int(select)
                    if select < 0 or select >= len(Tournament.t_list):
                        continue
                    break
                except ValueError:
                    continue

            print(f"Choose player to add to {Tournament.t_list[select].name}, {Tournament.t_list[select].location}: ")
            if not Player.p_list:
                print("*** No players available ***")
                input("Press ENTER to cancel\n")
            else:
                for i, p in enumerate(Player.p_list):
                    print(f'    [ {i} ] {p.surname}, {p.name}, {p.rank}')
                select = input("Select ? ")
