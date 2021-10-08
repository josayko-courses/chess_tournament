"""Display information about tournaments

"""

from models import Tournament
from .player_list import show_players
from .round_list import show_rounds
from views import error_msg


def select_tournament():
    tour_lst = [tour for tour in Tournament.t_list]
    if len(tour_lst) == 0:
        error_msg("No tournament available")
        return

    for i, t in enumerate(tour_lst):
        print(f'    [{i + 1}] {t.name}, {t.location}, {t.rating} === ', end="")
        nb = len(tour_lst[i].players)
        print(f'{nb}/8 Players')

    select = input("Select tournament: ")
    try:
        select = int(select) - 1
        if select < 0 or select >= len(Tournament.t_list):
            error_msg("invalid input")
            return None
    except ValueError:
        error_msg("invalid input")
        return None

    return select


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
    option = input("Select ? [1 ~ 2] ")
    try:
        option = int(option)
        if option != 1 and option != 2:
            error_msg("invalid input")
            return
    except ValueError:
        error_msg("invalid input")
        return

    if option == 1:
        players = [p[0] for p in Tournament.t_list[select].players]
        show_players(players)

    if option == 2:
        rounds = [r for r in Tournament.t_list[select].rounds]
        show_rounds(rounds)
