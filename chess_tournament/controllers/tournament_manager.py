"""Tournament Manager

"""

import os
from controllers import App
from models import Tournament, Player, Database


class TournamentManager:
    def create_tournament(input):
        # Add to db first and get id
        new_tournament = Tournament(
            0, input['name'], input['location'], input['rating'], input['desc'], input['start'], input['end']
        )
        App.tournaments.append(new_tournament)
        print(App.tournaments)
        return

    def add_player(index, tournament, dirname):
        players = App.players
        new_player = [players[index].id, 0]
        tournament.players.append(new_player)

        # Update database
        db = Database(dirname)
        db.add_player_to_tournament(new_player, tournament.id)
