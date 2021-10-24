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

        print(tournament)
        PlayerManager.create(
            {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank}, self.dirname
        )

        return
