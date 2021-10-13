""" Manage a chess tournament

with a Swiss-system for pairing the players
"""

import sys, os
from models import Player
from views import welcome, show_players, show_all_tournaments
from controllers import Application


def main():
    # Get db location and create app instance
    filepath = os.path.split(os.path.abspath(__file__))
    app = Application(filepath[0])
    app.load_db()

    while True:
        welcome()  # print welcome header on program start
        select = app.mm.main_menu()  # main menu selection
        if select == 1:
            app.tm.create_tournament()
        elif select == 2:
            app.pm.create_player()
        elif select == 3:
            app.tm.add_player()
        elif select == 4:
            app.generate_round()
        elif select == 5:
            app.add_results()
        elif select == 6:
            app.terminate_round()
        elif select == 7:
            show_all_tournaments()
        elif select == 8:
            show_players(Player.p_list)
        elif select == 9:
            app.pm.edit_player_rank()
        elif select == 0:  # quit the  program
            print('Quit')
            break
        else:
            continue

    return sys.exit(0)


if __name__ == "__main__":
    main()
