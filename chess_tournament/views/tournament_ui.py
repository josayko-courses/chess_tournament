"""Tournament related views

"""

from controllers import App
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

    def menu(id):
        t = App.tournaments[id]
        print("\n+=== Tournament Menu ===+")
        print(f"{t.name}, {t.location}, {t.rating}, {t.start}, {t.end}")
        print("+=======================+")
        while True:
            print("[0] Main Menu")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index)
                if index == 0:
                    return
                elif index >= 0 and index < 1:
                    continue
            except ValueError:
                continue

    def create(tournaments):
        print("+++++++ Create Tournament ++++++++")
