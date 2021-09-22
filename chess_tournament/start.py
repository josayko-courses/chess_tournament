""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament
from views import welcome
from controllers import Application as app
import sys


def main():

    players = []

    # print welcome header on program start
    welcome()
    while True:
        # main menu selection
        select = app.mm.main_menu()

        # create a new tournament
        if select == 1:
            new_tournament = app.tm.create_tournament()
            # TODO: Add data to the DB
            Tournament.t_list.append(new_tournament)
            print(Tournament.t_list)

        # quit the  program
        elif select == 0:
            print('Quit')
            break
        else:
            continue

    return sys.exit(0)


if __name__ == "__main__":
    main()
