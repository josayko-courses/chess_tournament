"""Tournament Manager

"""

from controllers import App
from models import Tournament, Player, Database


class TournamentManager:
    def add_player(index, tournament):
        players = App.players
        tournament.players.append([players[index].id, 0])
