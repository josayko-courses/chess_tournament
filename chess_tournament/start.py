""" Manage a chess tournament

with a Swiss-system for pairing the players
"""
from models import Tournament, Player
from views import welcome
from controllers import Application as app
import sys


def main():

    # Dummy data for tests
    test = Tournament('Tournoi test', 'Paris', 'blitz', 1, 'Created by the program')
    Tournament.t_list.append(test)

    p1 = Player('Player1', '', '', '', 1)
    p2 = Player('Player2', '', '', '', 2)
    p3 = Player('Player3', '', '', '', 3)
    p4 = Player('Player4', '', '', '', 4)
    p5 = Player('Player5', '', '', '', 5)
    p6 = Player('Player6', '', '', '', 6)
    p7 = Player('Player7', '', '', '', 7)
    p8 = Player('Player8', '', '', '', 8)
    Player.p_list.extend([p1, p2, p3, p4, p5, p6, p7, p8])
    test.players.extend([p1, p2, p3, p4, p5, p6, p7, p8])

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
