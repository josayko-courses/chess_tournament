"""Get tournament initialization details from User

"""

from models import Tournament


def create_tournament():
    """Get user input and return the data as a dictionary"""
    print("+ Create tournament +")
    # Rating choices, default is 'rapid'
    ratings = ('rapid', 'blitz', 'bullet')
    option = 0

    # Tournament name and location
    name = input("Enter tournament's name: ")
    location = input("Enter tournament's location: ")

    # Rating choice. Loop until user enter a valid option
    while True:
        rating = input("Rating type :\n    1 rapid\n    2 blitz\n    3 bullet\n    Rating ? (1-3, default=1) ")
        try:
            rating = int(rating)
            if rating > 0 and rating <= 3:
                option = int(option) - 1
                break
        except ValueError:
            continue

    # End date
    end = input("Enter length of the tournament : (days) ")

    # Description
    desc = input("Enter description : ")

    t = Tournament(name, location, ratings[option], int(end), desc)
    print(f">> Tournament created !")
    print(f">> Name: {name}")
    print(f">> Location: {location}")
    print(f">> Rating: {t.rating}")
    print(f">> From: {t.start}")
    print(f">> To: {t.end}")
    print(f">> Description: {t.desc}")
    print()

    return t