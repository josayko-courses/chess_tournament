"""Handle players information

"""

from models import Player


class PlayerManager:
    @staticmethod
    def create_player():
        """Get user input, create a new player and add it to the list"""

        print("+ Create player +")

        surname = input("Surname ? ")

        name = input("Name ? ")

        birthdate = input("Birth Date ? ")

        gender = input("Gender ? ")

        while True:
            rank = input("Rank ? (1 - 99+) ")
            try:
                rank = int(rank)
            except ValueError:
                continue
            if rank > 0:
                break

        p = Player(surname, name, birthdate, gender, rank)
        Player.p_list.append(p)

        print("New player created !")
        print(f">> Surname: {p.surname}")
        print(f">> Name: {p.name}")
        print(f">> Birth Date: {p.birthdate}")
        print(f">> Gender: {p.gender}")
        print(f">> Ranking: {p.rank}")
