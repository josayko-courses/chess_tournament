"""Get tournament initialization details from User

"""


def get_input():
    """Get user input and return the data as a dictionary"""
    name = input("Enter tournament's name: ")
    location = input("Enter tournament's location: ")
    rating = input("Enter rating type: ")
    end = input("Enter length of the tournament (days): ")
    return {'name': name, 'location': location, 'rating': rating, 'end': int(end)}
