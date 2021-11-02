"""Tournament Manager

"""

from controllers import App
from models import Tournament, Round


class TournamentManager:
    def start_tournament_error(tournament):
        if tournament.rounds:
            return "Tournament had already started"
        elif not tournament.players or len(tournament.players) % 2 != 0:
            return "Not enough players"
        return None

    def is_full(tournament):
        if len(tournament.players) >= 8:
            return True
        return False

    def add_player_check(index, tournament):
        if App.players[index].id not in tournament.get_players_ids():
            return None
        else:
            return f"{App.players[index]} is already registered to the tournament"

    def select_tournament_error(index):
        try:
            index = int(index) - 1
            if index < 0 or index >= len(App.tournaments):
                return True
        except ValueError:
            return True
        return False

    def menu_error(select):
        """Check user input form tournament menu"""
        try:
            select = int(select)
        except ValueError:
            return True
        return False

    def create_tournament_error(name, location, rating):
        if len(name) < 2:
            return "name input must be more than 1 character"
        elif len(location) < 2:
            return "location input must be more than 1 character"
        try:
            rating = int(rating) - 1
            if rating < 0 or rating > 2:
                return "rating input is invalid"
        except ValueError:
            return "rating input is invalid"
        return None

    def create_tournament(input, dirname):
        """Create a new tournament locally and save to db"""
        new_tournament = Tournament(
            0, input['name'], input['location'], input['rating'], input['desc'], input['start'], input['end']
        )
        new_tournament.id = new_tournament.save_tournament_to_db(dirname)
        App.tournaments.append(new_tournament)
        return

    def add_player(index, tournament, dirname):
        players = App.players
        new_player = [players[index].id, 0]
        tournament.players.append(new_player)
        tournament.update_tournament_players_db(new_player, tournament.id, dirname)

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
        tournament.update_tournament_rounds_db(new_round.serialize(), tournament.id, dirname)

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
        tournament.update_tournament_rounds_db(round.serialize(), tournament.id, dirname)

        return
