"""Tournament related functionnalities

"""
from models import Tournament


class TournamentManager:
    @staticmethod
    def create_tournament():
        """Get user input, create a new tournament and add it to the list"""

        print("+ Create tournament +")
        # Rating choices, default is 'rapid'
        ratings = ('rapid', 'blitz', 'bullet')
        option = 0

        # Tournament name and location
        name = input("Name ? ")
        location = input("Location ? ")

        # Rating choice. Loop until user enter a valid option
        while True:
            rating = input("Rating type :\n    1 rapid\n    2 blitz\n    3 bullet\n    Rating ? (1 - 3) ")
            try:
                rating = int(rating)
                if rating > 0 and rating <= 3:
                    option = int(option) - 1
                    break
            except ValueError:
                continue

        # End date
        end = input("Length ? (days) ")

        # Description
        desc = input("Description ? ")

        t = Tournament(name, location, ratings[option], int(end), desc)
        Tournament.t_list.append(t)

        print(f"New tournament created !")
        print(f">> Name: {t.name}")
        print(f">> Location: {t.location}")
        print(f">> Rating: {t.rating}")
        print(f">> From: {t.start}")
        print(f">> To: {t.end}")
        print(f">> Description: {t.desc}")
        print()
