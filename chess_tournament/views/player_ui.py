"""Player related views 

"""

from controllers import App, TournamentManager, PlayerManager
from bcolors import Color


class PlayerUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def select(self):
        while True:
            print("+++++++ Select player ++++++++")
            for i, t in enumerate(App.players):
                print(f"[{i + 1}] {t}")
            print(f"[0] Cancel")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index) - 1
                if index < -1 or index >= len(App.players):
                    continue
            except ValueError:
                continue
            return index

    def create(self, tournament):
        while True:
            print("+++++++ Create player ++++++++")
            surname = input("Surname ? ")
            name = input("Name ? ")
            birthdate = input("Birth Date ? ")
            gender = input("Gender ? ")
            rank = input("Rank ? ")
            try:
                rank = int(rank)
            except ValueError:
                return print("invalid input")

            PlayerManager.create(
                {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank},
                self.dirname,
            )
            print(f"{Color.OKGREEN}New {App.players[-1]} has been created{Color.ENDC}")

            if len(tournament.players) < 8:
                index = len(App.players) - 1
                while True:
                    select = input(f"Add new Player to this tournament ? (y/n, default=y) ")
                    if select.capitalize() == 'N':
                        break
                    elif not select or select.capitalize() == 'Y':
                        TournamentManager.add_player(index, tournament, self.dirname)
                        print(f"{Color.OKGREEN}{App.players[index]} has been registered to the tournament{Color.ENDC}")
                        break
            cancel = input("Add another player ? (y/n, default=y) ")
            if cancel.capitalize() == 'N':
                return -1
