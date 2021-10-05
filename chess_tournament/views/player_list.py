"""Display information about players

"""

from models import Player


def show_all_players():
    alpha_list = sorted(Player.p_list, key=lambda x: x.surname + x.name)

    for player in alpha_list:
        print(player.surname, player.name)

    print()
    input("Press ENTER to continue...")
