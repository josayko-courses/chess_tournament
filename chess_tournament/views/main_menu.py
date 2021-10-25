"""Main dashboard selection

"""

from bcolors import Color
from controllers import App


def main_menu():
    while True:
        print("\n+================================+")
        print("|                                |")
        print("|   Chess tournament manager     |")
        print("|                                |")
        print("+================================+\n")
        print("[1] Create Tournament")
        print("[2] Select Tournament")
        print("[3] All Tournaments Report")
        print("[9] Back")
        print("[0] Exit")
        select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
        try:
            select = int(select)
        except ValueError:
            continue
        return select


def all_tournaments_report():
    print("+++++++ All Tournaments report ++++++++")
    tournaments = App.tournaments
    players = App.players
    print(tournaments)
    print(players)
    return
