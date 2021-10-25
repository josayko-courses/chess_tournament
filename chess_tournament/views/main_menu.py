"""Main dashboard selection

"""

from bcolors import Color
from .player_ui import PlayerUI
from .tournament_ui import TournamentUI
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
    print(f"{Color.WARNING}+++++++ All Tournaments report ++++++++{Color.ENDC}")

    print(f"{Color.BOLD}\n+=== All players by rank ===+{Color.ENDC}")
    PlayerUI.print_players_by_rank(App.players)

    print(f"{Color.BOLD}\n+=== All players by name ===+{Color.ENDC}")
    PlayerUI.print_players_by_name(App.players)

    print(f"{Color.BOLD}\n+=== Tournaments ===+{Color.ENDC}")
    for t in App.tournaments:
        print(
            f"{Color.HEADER}| {t.id}. {t.name}, {t.location}, rating: {t.rating}, dates: {t.start} - {t.end} |{Color.ENDC}"
        )
        print(f"\"{t.desc}\"")
        print(f"{Color.BOLD}+ Players by rank +{Color.ENDC}")
        PlayerUI.print_players_by_rank(t.get_players_instance(App.players))

        print(f"{Color.BOLD}+ Players by name +{Color.ENDC}")
        PlayerUI.print_players_by_name(t.get_players_instance(App.players))

        print(f"{Color.BOLD}+ Players leaderboard +{Color.ENDC}")
        TournamentUI.print_leaderboard(t)
        print()
