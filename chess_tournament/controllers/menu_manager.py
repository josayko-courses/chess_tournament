"""Menu management

"""


class MenuManager:
    @staticmethod
    def main_menu():
        """Tournament monitoring dashboard"""
        while True:
            print("+========== Dashboard ===========+\n")
            print("    [ 1 ] Create a new tournament")
            print("    [ 2 ] Create a new player")
            print("    [ 3 ] Add player to tournament")
            print("    [ 4 ] Results")
            print("    [ 0 ] Quit\n")
            print("+================================+\n")
            select = input("Select ? (0 - 4) ")
            print()
            try:
                val = int(select)
                return val
            except ValueError:
                print("*** Error: invalid input ***")
                input("Press ENTER to continue...")
                continue
