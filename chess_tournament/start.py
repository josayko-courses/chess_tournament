""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament
from views import get_input, dashboard, welcome
import sys


def main():

    welcome()
    input = get_input()
    t = Tournament(input['name'], input['location'], input['rating'], input['end'])
    print(t)
    dashboard()
    return sys.exit(0)


if __name__ == "__main__":
    main()
