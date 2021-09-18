"""Get tournament initialization details from User

"""


def get_input():
    name = input("Enter tournament's name: ")
    location = input("Enter tournament's location: ")
    rating = input("Enter rating type: ")
    end = input("Enter length of the tournament (days): ")
    return {'name': name, 'location': location, 'rating': rating, 'end': int(end)}
