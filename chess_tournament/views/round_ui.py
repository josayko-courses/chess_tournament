"""Round related views

"""

from controllers import App
from bcolors import Color


class RoundUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def print_games(self, tournament, games):
        players = tournament.get_players_instance(App.players)
        for i, game in enumerate(games):
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
                if game_index < 0 or game_index > last_index:
                    continue
                break
            except ValueError:
                continue
        return game_index

    def select_result(self):
        return

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
        print("+++++++ Edit round ++++++++")
        if len(tournament.rounds) == 0:
            return print(f"{Color.FAIL}Please start tournament first{Color.FAIL}")
        elif tournament.rounds[-1].end:
            return print(f"{Color.FAIL}The tournament is over{Color.FAIL}")

        games = tournament.rounds[-1].games
        last_index = self.print_games(tournament, games)
        game_index = self.select_game(last_index)

        game = games[game_index]
        players = tournament.get_players_instance(App.players)
        g = self.get_games_with_players_instance(game, players)
        print(f"{Color.WARNING}Edit results for Game {game_index + 1}{Color.ENDC}: ")
        print(f"[1] id: {g[0][0].id}, {g[0][0].surname} {g[0][0].name} {Color.OKGREEN}win{Color.ENDC}")
        print(f"[2] id: {g[1][0].id}, {g[1][0].surname} {g[1][0].name} {Color.OKGREEN}win{Color.ENDC}")
        print("[3] Draw game")
        print("[4] Reset results")
        print("[0] Cancel")
        return

    def terminate(self, tournament):
        print("+++++++ Terminate round ++++++++")
        return