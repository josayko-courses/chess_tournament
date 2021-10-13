"""Menu management

"""

from views import error_msg


class MenuManager:
    @staticmethod
    def main_menu():
        """Tournament monitoring dashboard"""
        while True:
            print("+========== Dashboard ===========+\n")
            print("    [1] Create a new tournament")
            print("    [2] Create a new player")
            print("    [3] Register player to tournament")

            print("    [4] Generate round")
            print("    [5] Add results")
            print("    [6] Terminate round")

            print("    [7] Tournament information")
            print("    [8] Player information")
            print("    [9] Edit player rank")
            print("    [0] Quit\n")
            print("+================================+\n")
            select = input("Select ? [0 ~ 9] ")

            try:
                val = int(select)
                return val
            except ValueError:
                error_msg("invalid input")
                continue
