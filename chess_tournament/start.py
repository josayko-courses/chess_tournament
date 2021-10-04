""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament, Player
from views import welcome
from controllers import Application
import sys, os


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

        elif select == 0:  # quit the  program
            print('Quit')
            break

        elif select == 2:
            app.pm.create_player()

        elif select == 3:
            app.tm.add_player()

        elif select == 4:
            app.generate_round(Tournament.t_list[0].players)

        else:
            continue

    return sys.exit(0)


if __name__ == "__main__":
    main()
