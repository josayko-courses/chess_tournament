"""Round related views

"""

from controllers import App, TournamentManager, RoundManager
from bcolors import Color


class RoundUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def print_games(self, tournament, games):
        players = tournament.get_players_instance(App.players)
        for i, game in enumerate(games):
            p1 = ""
            p2 = ""
            for p in players:
                if game[0][0] == p.id:
                    p1 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[0][1]}"
                if game[1][0] == p.id:
                    p2 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[1][1]}"
            print(f"Game {i + 1} | {p1} vs. {p2}")
        return i

    def select_game(self, last_index):
        while True:
            game_index = input("Game nb. ? ")
            try:
                game_index = int(game_index) - 1
                if game_index < -1 or game_index > last_index:
                    continue
                break
            except ValueError:
                continue
        return game_index

    def select_result(self, game_index, g):
        while True:
            print(f"{Color.WARNING}Edit results for Game {game_index + 1}{Color.ENDC}: ")
            print(f"    [1] id: {g[0][0].id}, {g[0][0].surname} {g[0][0].name} {Color.OKGREEN}win{Color.ENDC}")
            print(f"    [2] id: {g[1][0].id}, {g[1][0].surname} {g[1][0].name} {Color.OKGREEN}win{Color.ENDC}")
            print("    [3] Draw game")
            print("    [4] Reset results")
            print("    [0] Cancel")
            result = input("Result ? ")
            try:
                result = int(result)
                if result < 0 or result > 4:
                    continue
                break
            except ValueError:
                continue
        return result

    def get_games_with_players_instance(self, game, players):
        detailed_game = []

        for p in players:
            if p.id == game[0][0]:
                p1 = [p, game[0][1]]
            if p.id == game[1][0]:
                p2 = [p, game[1][1]]
        detailed_game.append(p1)
        detailed_game.append(p2)
        return detailed_game

    def edit(self, tournament):
        error = RoundManager.edit_round_error(tournament)
        if error:
            return print(f"{Color.FAIL}{error}{Color.ENDC}")

        games = tournament.rounds[-1].games
        while True:
            print("+++++++ Edit round ++++++++")
            print(f"{Color.WARNING}Select Game nb. or nb. [0] to Cancel...{Color.ENDC}")
            last_index = self.print_games(tournament, games)
            game_index = self.select_game(last_index)
            if game_index == -1:
                return -1

            players = tournament.get_players_instance(App.players)
            g = self.get_games_with_players_instance(games[game_index], players)
            result = self.select_result(game_index, g)
            if result != 0:
                RoundManager.update_results(self.dirname, result, games, game_index, tournament)
                print(f"{Color.OKGREEN}Results updated{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
                continue

    def terminate(self, tournament):
        print("+++++++ Terminate round ++++++++")
        error = RoundManager.terminate_round_error(tournament)
        if error:
            return print(f"{Color.FAIL}{error}{Color.ENDC}")
        RoundManager.terminate_round(self.dirname, tournament)

        # Create next round
        print(f"{Color.WARNING}Ending current round. Creating next round with new games...{Color.ENDC}")
        error = RoundManager.create_next_round(tournament, self.dirname)
        if error:
            return print(f"{Color.FAIL}{error}{Color.ENDC}")
        print(f"{Color.WARNING}{tournament.rounds[-1].name} start... {Color.ENDC}")

        # Print games info
        players = tournament.get_players_instance(App.players)
        print(f"{Color.WARNING}Next games: ")
        for i, game in enumerate(tournament.rounds[-1].games):
            for p in players:
                if game[0][0] == p.id:
                    p1 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}"
                if game[1][0] == p.id:
                    p2 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}"
            print(f"Game {i + 1} | {p1} vs. {p2}")
        print(f"{Color.ENDC}", end="")

    def print_rounds(rounds):
        win = Color.OKGREEN
        end = Color.ENDC
        for r in rounds:
            print(f"{Color.WARNING}{r.name}, start: {r.start}, end: {r.end}{Color.ENDC}")
            for i, game in enumerate(r.games):
                for p in App.players:
                    if game[0][0] == p.id:
                        if game[0][1] == 1:
                            p1 = f"{win}id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[0][1]}{end}"
                        else:
                            p1 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[0][1]}"
                    if game[1][0] == p.id:
                        if game[1][1] == 1:
                            p2 = f"{win}id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[1][1]}{end}"
                        else:
                            p2 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}, score: {game[1][1]}"
                print(f"Game {i + 1} | {p1} vs. {p2}")
        return
