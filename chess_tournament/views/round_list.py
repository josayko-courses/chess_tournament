"""Display rounds information

"""

from .main_view import error_msg


def show_rounds(rounds):
    if not rounds:
        return error_msg("There is no round generated")
    for index, round in enumerate(rounds):
        print(f"    [{index + 1}] {round.name}")
    select = input("Enter round number: ")
    try:
        select = int(select) - 1
        if select < 0 or select >= len(rounds):
            return error_msg("invalid input")
    except ValueError:
        error_msg("invalid input")
        return

    print(f"Name: {rounds[select].name}")
    print(f"Start: {rounds[select].start}")
    print(f"End: {rounds[select].end}")
    for i, game in enumerate(rounds[select].games):
        print(
            f"    Game {i + 1}: {game[0][0].surname}, {game[0][0].name} <rank: {game[0][0].rank}, score: {game[0][1]}> ",
            end="",
        )
        print(f"vs. {game[1][0].surname}, {game[1][0].name}, <rank: {game[1][0].rank}, score: {game[1][1]}>")

    input("Press ENTER to continue...\n")
