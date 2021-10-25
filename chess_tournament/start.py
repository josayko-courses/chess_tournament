"""Program launcher

chess tournament
"""

import sys
import os
from controllers import App
from views import main_menu, TournamentUI
from bcolors import Color


def main_loop(options, tournament):
    while True:
        index = main_menu()
        if index == 0:
            print(options[index])
            break
        elif index >= 0 and index < 3:
            i = options[index]()
            if id is not None:
                tournament.menu(i)
            else:
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")


def main():
    filename = os.path.split(os.path.abspath(__file__))
    App.program_initialization(filename[0])
    tournament = TournamentUI(filename[0])
    options = ["Exit", tournament.create, tournament.select]

    if App.tournaments:
        tournament.menu(len(App.tournaments) - 1)
    main_loop(options, tournament)
    return sys.exit(0)


if __name__ == "__main__":
    main()
