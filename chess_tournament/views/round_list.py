"""Display rounds information

"""

from .main_view import error_msg


def show_rounds(rounds):
    for index, round in enumerate(rounds):
        print(f"    [{index + 1}] {round.name}")
    select = input("Enter round number: ")
    try:
        select = int(select) - 1
        if select < 0 or select >= len(rounds):
            error_msg("invalid input")
            return
    except ValueError:
        error_msg("invalid input")
        return

    print(f"Name: {rounds[select].name}")
    print(f"Start: {rounds[select].start}")
    print(f"End: {rounds[select].end}")
    for game in rounds[select].games:
        print(f"{game[0][0]} [score: {game[0][1]}] vs. {game[1][0]}")

    input("Press ENTER to continue...\n")
