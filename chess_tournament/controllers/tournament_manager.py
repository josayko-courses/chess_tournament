"""Tournament Manager

"""

import os
from controllers import App
from models import Tournament, Player, Database


class TournamentManager:
    def add_player(index, tournament, dirname):
        players = App.players
        tournament.players.append([players[index].id, 0])
        print(dirname)
