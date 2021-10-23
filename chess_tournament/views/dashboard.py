"""Main dashboard selection

"""


def menu():
    select = input("Select ? ")
    try:
        select = int(select)
    except ValueError:
        return
    return select
