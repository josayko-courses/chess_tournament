"""Main dashboard selection

"""

from bcolors import Color


def main_menu():
    while True:
        print("\n+================================+")
        print("|                                |")
        print("|   Chess tournament manager     |")
        print("|                                |")
        print("+================================+\n")
        print("[1] Create Tournament")
        print("[2] Select Tournament")
        print("[0] Exit")
        select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
        try:
            select = int(select)
        except ValueError:
            continue
        return select
