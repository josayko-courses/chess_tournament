""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament
from views import dashboard, welcome
from controllers import Application as app
import sys


def main():

    players = []

    welcome()
    while True:
        select = dashboard()
        if select == 1:
            new_tournament = app.tm.create_tournament()
            # TODO: Add data to the DB
            Tournament.t_list.append(new_tournament)
            print(Tournament.t_list)
        elif select == 0:
            print('Quit')
            break
        else:
            continue
    return sys.exit(0)


if __name__ == "__main__":
    main()
