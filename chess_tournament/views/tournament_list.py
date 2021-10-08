"""Display information about tournaments

"""

from models import Tournament
from .player_list import show_players
from views import error_msg


def show_all_tournaments():
    print("+ Tournament list +")
    for i, t in enumerate(Tournament.t_list):
        print(f'    [{i + 1}] {t.name}, {t.location}, {t.rating} === ', end="")
        nb = len(Tournament.t_list[i].players)
        print(f'{nb}/8 Players')
    select = input("Select tournament: ")
    try:
        select = int(select) - 1
        if select < 0 or select >= len(Tournament.t_list):
            error_msg("invalid input")
            return
    except ValueError:
        error_msg("invalid input")
        return

    print(f"Choose option for {Tournament.t_list[select].name}, {Tournament.t_list[select].location}: ")
    print("[1] players")
    print("[2] rounds")
    print("[3] games")
    option = input("Select ? [1 ~ 3] ")
    try:
        option = int(option)
    except ValueError:
        error_msg("invalid input")
        return

    if option == 1:
        players = [p[0] for p in Tournament.t_list[select].players]
        show_players(players)
