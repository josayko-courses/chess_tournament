"""Tournament Manager

"""

from controllers import App
from models import Tournament, Player, Database


class TournamentManager:
    def create_tournament(input, dirname):
        # Add to db first and get id
        db = Database(dirname)
        id = db.create_tournament(input)

        # Update local data
        new_tournament = Tournament(
            id, input['name'], input['location'], input['rating'], input['desc'], input['start'], input['end']
        )
        App.tournaments.append(new_tournament)
        return

    def add_player(index, tournament, dirname):
        players = App.players
        new_player = [players[index].id, 0]
        tournament.players.append(new_player)

        # Update database
        db = Database(dirname)
        db.add_player_to_tournament(new_player, tournament.id)
