"""Program launcher

chess tournament
"""

import sys
import os
from views import menu
from controllers import App


def main():
    filename = os.path.split(os.path.abspath(__file__))
    App.program_initialization(filename[0])
    while True:
        print("+===+ Chess tournament +===+")
        select = menu()
        if select == 0:
            break
    return sys.exit(0)


if __name__ == "__main__":
    main()
