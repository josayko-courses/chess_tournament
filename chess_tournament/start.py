"""Program launcher

chess tournament
"""

import sys
import os
from controllers import App
from views import main_menu, all_tournaments_report, TournamentUI
from bcolors import Color


def main_loop(options, tournament):
    """Main menu loop"""
    while True:
        index = main_menu()
        if index == 0:
            print(options[index])
            break
        if index == 9:
            if App.tournaments:
                tournament.menu(len(App.tournaments) - 1)
        elif index >= 0 and index < 5:
            i = options[index]()
            if i is not None:
                tournament.menu(i)
            else:
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")


def main():
    """Main function, program initialization"""
    filename = os.path.split(os.path.abspath(__file__))
    App.program_initialization(filename[0])
    tournament = TournamentUI(filename[0])
    options = ["Exit", tournament.create, tournament.select, all_tournaments_report, tournament.edit_player_rank]

    if App.tournaments:
        if not App.tournaments[-1].rounds or not App.tournaments[-1].rounds[-1].end:
            tournament.menu(len(App.tournaments) - 1)
    else:
        print(f"{Color.WARNING}No tournament available...{Color.ENDC}")
        i = tournament.create()
        if i is not None:
            tournament.menu(i)
    main_loop(options, tournament)
    return sys.exit(0)


if __name__ == "__main__":
    main()
