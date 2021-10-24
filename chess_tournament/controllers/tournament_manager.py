"""Tournament Manager

"""

from controllers import App
from models import Tournament, Round, Database


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

    def create_first_round(tournament, dirname):
        # sort players by rank
        players = tournament.get_players(App.players)
        players_by_rank = sorted(players, key=lambda x: x.rank)

        # create pairs locally
        half = int(len(players) / 2)
        first_half = players_by_rank[:half]
        second_half = players_by_rank[half:]
        pairs = zip(first_half, second_half)
        games = []
        for p in pairs:
            new_game = [[p[0].id, 0], [p[1].id, 0]]
            games.append(new_game)
        new_round = Round("Round 1", games)
        tournament.rounds.append(new_round)

        # update DB
        db = Database(dirname)
        db.add_round_to_tournament(new_round.serialize(), tournament.id)
