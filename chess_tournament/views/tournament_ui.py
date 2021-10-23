"""Tournament related views

"""

from controllers import App, TournamentManager
from bcolors import Color
from views import PlayerUI


class TournamentUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def select(self):
        """Tournament list selection"""
        while True:
            print("+++++++ Select tournament ++++++++")
            for i, t in enumerate(App.tournaments):
                print(f"[{i + 1}] {t}")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index) - 1
                if index < 0 or index >= len(App.tournaments):
                    continue
            except ValueError:
                continue
            return index

    def menu(self, id):
        """Tournament menu"""
        t = App.tournaments[id]

        options = ["Exit", self.add_player]
        while True:
            print("\n+=== Tournament Menu ===+")
            print(f"{t.name}, {t.location}, {t.rating}, {t.start}, {t.end}")
            print("+=======================+")
            print("[1] Add player")
            print("[0] Main Menu")
            select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                select = int(select)
                if select == 0:
                    return
                elif select > 0 and select < 2:
                    if options[select](t) is None:
                        input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            except ValueError:
                continue

    def create(self):
        print("+++++++ Create Tournament ++++++++")
        App.create_tournament()

    def add_player(self, tournament):
        print("+++++++ Add Player ++++++++")
        while True:
            if len(tournament.players) >= 8:
                print(f"{Color.FAIL}This tournament is full{Color.ENDC}")
                index = None
                break
            players_ids = [x[0] for x in tournament.players]
            print(f"Registered players ids: {players_ids}")
            index = PlayerUI.select()
            if index == -1:
                break
            if App.players[index].id not in players_ids:
                TournamentManager.add_player(index, tournament, self.dirname)
                print(f"{Color.OKGREEN}{App.players[index]} successfully registered to the tournament{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            else:
                print(f"{Color.FAIL}{App.players[index]} is already registered to the tournament{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
        return index
