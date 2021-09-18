""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament
import sys


def main(argv):
    if len(argv) >= 3:
        print("\n--- Chess tournament manager ---\n")
        if len(argv) == 4:
            nb_days = int(argv[3]) - 1
            end = 0 if nb_days <= 0 else nb_days
            t = Tournament(argv[1], argv[2], end)
        else:
            t = Tournament(argv[1], argv[2])
        print(t.name, t.location, t.start, t.end)
    else:
        print('Usage: start.py [NAME] [LOCATION] [END_DATE]')
    return sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
