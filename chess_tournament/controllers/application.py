"""Get tournament initialization details from User

"""

from .tournament_manager import TournamentManager
from .menu_manager import MenuManager
from .player_manager import PlayerManager


class Application:
    tm = TournamentManager
    mm = MenuManager
    pm = PlayerManager
