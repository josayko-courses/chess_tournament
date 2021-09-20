"""Get tournament initialization details from User

"""


def get_input():
    """Get user input and return the data as a dictionary"""
    # Rating choices, default is 'rapid'
    ratings = ('rapid', 'blitz', 'bullet')
    option = 0

    # Tournament name and location
    name = input("Enter tournament's name: ")
    location = input("Enter tournament's location: ")

    # Rating choice
    rating = input("Rating type :\n    1 rapid\n    2 blitz\n    3 bullet\n    Rating ? (1-3, default=1) ")
    if int(rating) > 0 and int(rating) <= 3:
        option = int(option) - 1

    # End date
    end = input("Enter length of the tournament : (days) ")

    return {'name': name, 'location': location, 'rating': ratings[option], 'end': int(end)}
