"""Main menu for tournament management

"""


def welcome():
    """Print the program welcome header"""
    print("\n+================================+")
    print("|                                |")
    print("|   Chess tournament manager     |")
    print("|                                |")
    print("+================================+\n")


def error_msg(str):
    print("Error: " + str)
    input("Press ENTER to cancel...")
    return 0
