""" Manage a chess tournament

with a Swiss-system for pairing the players
"""

import sys, os
from models import Tournament, Player
from views import welcome, show_players, show_all_tournaments
from controllers import Application


def main():
    # Get db location and create app instance
    filepath = os.path.split(os.path.abspath(__file__))
    app = Application(filepath[0])
    app.load_db()

    welcome()  # print welcome header on program start
    while True:
        select = app.mm.main_menu()  # main menu selection

        # create a new tournament
        if select == 1:
            app.tm.create_tournament()

        elif select == 2:
            app.pm.create_player()

        elif select == 3:
            app.tm.add_player()

        elif select == 4:
            app.generate_round()

        elif select == 6:
            show_all_tournaments()

        elif select == 7:
            show_players(Player.p_list)

        elif select == 0:  # quit the  program
            print('Quit')
            break
        else:
            continue

    return sys.exit(0)


if __name__ == "__main__":
    main()
