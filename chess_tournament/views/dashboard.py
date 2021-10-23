"""Main dashboard selection

"""


def menu():
    print("\n+================================+")
    print("|                                |")
    print("|   Chess tournament manager     |")
    print("|                                |")
    print("+================================+\n")
    select = input("Select ? ")
    try:
        select = int(select)
    except ValueError:
        return
    return select
