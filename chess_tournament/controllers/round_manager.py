"""Round Manager

"""

from datetime import datetime
from .tournament_manager import TournamentManager


class RoundManager:
    def edit_round_error(tournament):
        """Checks errors when editing round results"""
        if len(tournament.rounds) == 0:
            return "Please start tournament first"
        elif tournament.rounds[-1].end:
            return "The tournament is over"
        return None

    def terminate_round_error(tournament):
        """Checks errors when setting round as finished"""
        if len(tournament.rounds) == 0:
            return "Please start tournament first"
        elif tournament.rounds[-1].end:
            return "The tournament is over"
        for game in tournament.rounds[-1].games:
            if game[0][1] == 0 and game[1][1] == 0:
                return "Cannot terminate round: all games must have a result"
        return None

    def create_next_round(tournament, dirname):
        """Create next round"""
        if len(tournament.rounds) >= tournament.nb_rounds:
            return "Maximum nb of rounds (4) reached. Tournament is over"
        if TournamentManager.create_next_round(dirname, tournament) == -1:
            return "All possible games have been played: tournament is over"

    def terminate_round(dirname, tournament):
        """Set round as finished andupdate db"""
        tournament.rounds[-1].end = datetime.today().strftime('%Y-%m-%d %H:%M')
        tournament.update_round_end_db(tournament, dirname)

    def reset_game_results(game, player1, player2):
        """Reset game results to 0 for both players"""
        if game[0][1] == 1:
            player1[1] -= 1
        elif game[0][1] == 0.5:
            player1[1] -= 0.5
        if game[1][1] == 1:
            player2[1] -= 1
        elif game[1][1] == 0.5:
            player2[1] -= 0.5
        game[0][1] = 0
        game[1][1] = 0
        return

    def update_results(dirname, result, games, game_index, tournament):
        """Update game results and players scores. Then update in db"""
        # Get players total score reference
        game = games[game_index]
        for p in tournament.players:
            if p[0] == game[0][0]:
                player1 = p
            if p[0] == game[1][0]:
                player2 = p

        # Update game score + individual score
        RoundManager.reset_game_results(game, player1, player2)
        if result == 1:
            player1[1] += 1
            game[0][1] = 1
            game[1][1] = 0
        elif result == 2:
            player2[1] += 1
            game[0][1] = 0
            game[1][1] = 1
        elif result == 3:
            player1[1] += 0.5
            player2[1] += 0.5
            game[0][1] = 0.5
            game[1][1] = 0.5

        tournament.update_tournament_results_db(game, game_index, player1, player2, dirname)
        return
