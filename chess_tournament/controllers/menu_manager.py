"""Menu management

"""


class MenuManager:
    @staticmethod
    def main_menu():
        """Tournament monitoring dashboard"""
        while True:
            print("+========== Dashboard ===========+\n")
            print("    1 Create a new tournament")
            print("    2 Create a new player")
            print("    0 Quit\n")
            print("+================================+\n")
            select = input("Select ? (0 - 2) ")
            print()
            try:
                val = int(select)
                return val
            except ValueError:
                continue
