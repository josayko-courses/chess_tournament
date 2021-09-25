""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament, Player
from views import welcome
from controllers import Application as app
import sys


def main():

    players = []

    welcome()  # print welcome header on program start
    while True:
        select = app.mm.main_menu()  # main menu selection

        # create a new tournament
        if select == 1:
            app.tm.create_tournament()
            print(Tournament.t_list)

        elif select == 0:  # quit the  program
            print('Quit')
            break
        elif select == 2:
            app.pm.create_player()
            print(Player.p_list)
        else:
            continue

    return sys.exit(0)


if __name__ == "__main__":
    main()
