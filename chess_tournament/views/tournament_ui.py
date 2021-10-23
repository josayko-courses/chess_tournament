"""Tournament related views

"""

from controllers import App, TournamentManager
from bcolors import Color


class TournamentUI:
    def select():
        while True:
            for i, t in enumerate(App.tournaments):
                print(f"[{i + 1}] {t}")
            select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                select = int(select) - 1
                if select < 0 or select >= len(App.tournaments):
                    continue
            except ValueError:
                continue
            return select

    @classmethod
    def menu(cls, id):
        t = App.tournaments[id]

        options = ["Exit", cls.add_player]
        while True:
            print("\n+=== Tournament Menu ===+")
            print(f"{t.name}, {t.location}, {t.rating}, {t.start}, {t.end}")
            print("+=======================+")
            print("[1] Add player")
            print("[0] Main Menu")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index)
                if index == 0:
                    return
                elif index > 0 and index < 2:
                    options[index]()
                    input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            except ValueError:
                continue

    def create():
        print("+++++++ Create Tournament ++++++++")
        App.create_tournament()

    def add_player():
        TournamentManager.add_player()
        return
