"""Program launcher

chess tournament
"""

import sys
import os
from views import menu
from controllers import App, TournamentManager


def main():
    filename = os.path.split(os.path.abspath(__file__))
    App.program_initialization(filename[0])
    print(App.players)
    print(App.tournaments)

    options = ["Exit", TournamentManager.create_tournament]
    while True:
        index = menu()
        if index == 0:
            print(options[index])
            break
        else:
            options[index]()
    return sys.exit(0)


if __name__ == "__main__":
    main()
