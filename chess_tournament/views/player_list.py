"""Display information about players

"""

from views import error_msg


def show_players(players):
    print("+ Player information +")
    select = input("Players sorted by :\n    [1] alphabetical order\n    [2] rank order\n    Select ? [1 ~ 2] ")

    try:
        select = int(select)
    except ValueError:
        return error_msg("invalid input")

    if select == 1:
        alpha_list = sorted(players, key=lambda x: x.surname + x.name)
        for player in alpha_list:
            print(
                f"id: {player.id}, name: {player.surname} {player.name}, birthdate: {player.birthdate}, gender: {player.gender}, rank: {player.rank}"
            )
    elif select == 2:
        rank_list = sorted(players, key=lambda x: x.rank)
        for player in rank_list:
            print(
                f"id: {player.id}, name: {player.surname} {player.name}, birthdate: {player.birthdate}, gender: {player.gender}, rank: {player.rank}"
            )
    else:
        return error_msg("invalid input")

    input("Press ENTER to continue...")
