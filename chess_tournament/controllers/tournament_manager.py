"""Tournament Manager

"""

from controllers import App
from models import Tournament, Round, Database


class TournamentManager:
    def create_error(name, location, rating):
        if len(name) < 2:
            return "input must be more than 1 character"
        elif len(location) < 2:
            return "input must be more than 1 character"
        try:
            rating = int(rating) - 1
            if rating < 0 or rating > 2:
                return "invalid input"
        except ValueError:
            return "invalid input"
        return None

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
        players = tournament.get_players_instance(App.players)
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

    def create_next_round(dirname, tournament):
        # 1st step: sort by scores
        players = tournament.get_players_with_score(App.players)
        sorted_players = sorted(players, key=lambda x: x[1], reverse=True)

        # 2nd step: bubble sort, if scores are equals, sort by rank (ascending)
        i = 1
        while i < len(sorted_players):
            if sorted_players[i][1] == sorted_players[i - 1][1]:
                if sorted_players[i][0].rank < sorted_players[i - 1][0].rank:
                    sorted_players[i], sorted_players[i - 1] = sorted_players[i - 1], sorted_players[i]
                    i = 1
                    continue
            i += 1

        # Get all previous games combinations
        combos = []
        for r in tournament.rounds:
            for g in r.games:
                combos.append([g[0][0], g[1][0]])

        # Create new pairings
        p_ids = [x[0].id for x in sorted_players]
        pairing = []
        counter = len(p_ids)
        while len(p_ids) >= 2:
            p1 = p_ids[0]
            i = 1
            if len(p_ids) == 2:
                p2 = p_ids[i]
                pairing.append([p1, p2])
                p_ids.remove(p1)
                p_ids.remove(p2)
                break
            while i < len(p_ids):
                p2 = p_ids[i]
                if p1 != p2 and [p1, p2] not in combos and [p2, p1] not in combos:
                    pairing.append([p1, p2])
                    p_ids.remove(p1)
                    p_ids.remove(p2)
                    break
                i += 1
            counter -= 1
            if counter == 0:
                return -1

        # Create games
        next_games = []
        for p in pairing:
            p1 = [x[0].id for x in sorted_players if x[0].id == p[0]]
            p2 = [x[0].id for x in sorted_players if x[0].id == p[1]]
            next_games.append([[p1[0], 0], [p2[0], 0]])

        # Create new round
        nb = len(tournament.rounds) + 1
        round = Round(f"Round {nb}", next_games)
        tournament.rounds.append(round)

        # Update db
        db = Database(dirname)
        db.add_round_to_tournament(round.serialize(), tournament.id)
        return
