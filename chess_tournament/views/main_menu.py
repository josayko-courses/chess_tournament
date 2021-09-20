"""Main menu for tournament management

"""


def welcome():
    """Print the program welcome header"""
    print("\n+================================+")
    print("|                                |")
    print("|   Chess tournament manager     |")
    print("|                                |")
    print("+================================+\n")


def dashboard():
    """Tournament monitoring dashboard"""
    while True:
        print("+========== Dashboard ===========+\n")
        print("    1 Create a new tournament")
        print("    0 Quit\n")
        print("+================================+\n")
        select = input("Select: (0-1) ")
        print()
        try:
            val = int(select)
            return val
        except ValueError:
            continue
