"""Display information about players

"""


def show_players(players):
    print("+ Player list +")
    select = input("Players sorted by :\n    [1] alphabetical order\n    [2] rank order\n    Select ? [1 ~ 2] ")
    print()

    try:
        select = int(select)
    except ValueError:
        print("Error: invalid input")
        input("Press ENTER to cancel...")
        return

    if select == 1:
        alpha_list = sorted(players, key=lambda x: x.surname + x.name)
        for player in alpha_list:
            print(f"[id: {player.id}] [rank: {player.rank}] {player.surname}, {player.name}")
    elif select == 2:
        rank_list = sorted(players, key=lambda x: x.rank)
        for player in rank_list:
            print(f"[id: {player.id}] [rank: {player.rank}] {player.surname}, {player.name}")
    else:
        print("Error: invalid input")
        input("Press ENTER to cancel...")
        return

    print()
    input("Press ENTER to continue...")
