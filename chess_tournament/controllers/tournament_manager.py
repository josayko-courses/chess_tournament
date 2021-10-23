"""Tournament Manager

"""

import os
from controllers import App
from models import Tournament, Player, Database


class TournamentManager:
    def add_player(index, tournament, dirname):
        players = App.players
        new_player = [players[index].id, 0]
        tournament.players.append(new_player)

        # Update database
        db = Database(dirname)
        db.add_player_to_tournament(new_player, tournament.id)
