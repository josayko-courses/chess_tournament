""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament
from views import dashboard, welcome
from controllers import create_tournament
import sys


def main():

    welcome()
    while True:
        select = dashboard()
        if select == 1:
            t = create_tournament()
            print(t)
        elif select == 0:
            print('Quit')
            break
        else:
            continue
    return sys.exit(0)


if __name__ == "__main__":
    main()
