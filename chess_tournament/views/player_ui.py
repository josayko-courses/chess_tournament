"""Player related views 

"""

from controllers import App
from bcolors import Color


class PlayerUI:
    def select():
        while True:
            print("+++++++ Select player ++++++++")
            for i, t in enumerate(App.players):
                print(f"[{i + 1}] {t}")
            print(f"[0] Cancel")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index) - 1
                if index < -1 or index >= len(App.players):
                    continue
            except ValueError:
                continue
            return index
