"""Tournament related views

"""

import sys
from controllers import App, TournamentManager
from bcolors import Color
from views import PlayerUI


class TournamentUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def select(self):
        """Tournament list selection"""
        if not App.tournaments:
            return print(f"{Color.FAIL}No tournament{Color.FAIL}")
        while True:
            print("+++++++ Select tournament ++++++++")
            for i, t in enumerate(App.tournaments):
                print(f"[{i + 1}] {t}")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                index = int(index) - 1
                if index < 0 or index >= len(App.tournaments):
                    continue
            except ValueError:
                continue
            return index

    def start(self, tournament):
        if tournament.rounds:
            return print(f"{Color.FAIL}Tournament had already started{Color.ENDC}")
        elif not tournament.players or len(tournament.players) % 2 != 0:
            return print(f"{Color.FAIL}Not enough players{Color.ENDC}")
        TournamentManager.create_first_round(tournament, self.dirname)
        print(f"{Color.OKGREEN}Tournament sucessfully started at {tournament.rounds[0].start}{Color.ENDC}")
        players = tournament.get_players(App.players)

        # Print games info
        print(f"{Color.WARNING}Next games: ")
        for i, game in enumerate(tournament.rounds[0].games):
            for p in players:
                if game[0][0] == p.id:
                    p1 = f"{p.surname} {p.name}, rank: {p.rank}"
                if game[1][0] == p.id:
                    p2 = f"{p.surname} {p.name}, rank: {p.rank}"
            print(f"Game {i + 1} | {p1} vs. {p2}")
        print(f"{Color.ENDC}", end="")

    def menu(self, id):
        """Tournament menu"""
        t = App.tournaments[id]
        player = PlayerUI(self.dirname)

        options = ["Exit", self.start, player.create, self.add_player]
        while True:
            print("\n+=== Tournament Menu ===+")
            print(f"{t.name}, {t.location}, {t.rating}, {t.start}, {t.end}")
            print("+=======================+")
            print("[1] Start")
            print("[2] Create Player")
            print("[3] Add player")
            print("[9] Main menu")
            print("[0] Exit")
            select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                select = int(select)
                if select == 0:
                    sys.exit(0)
                elif select == 9:
                    return
                elif select > 0 and select < 4:
                    if options[select](t) is None:
                        input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            except ValueError:
                continue

    def create(self):
        print("+++++++ Create Tournament ++++++++")
        ratings = ('rapid', 'blitz', 'bullet')
        name = input("Name ? ")
        if len(name) < 2:
            return print(f"{Color.FAIL}input must be more than 1 character{Color.FAIL}")
        location = input("Location ? ")
        if len(location) < 2:
            return print(f"{Color.FAIL}input must be more than 1 character{Color.FAIL}")
        rating = input("Rating type :\n    [1] rapid\n    [2] blitz\n    [3] bullet\n    Rating ? ")
        try:
            rating = int(rating) - 1
            if rating < 0 or rating > 2:
                return print(f"{Color.FAIL}invalid input{Color.FAIL}")
        except ValueError:
            return print(f"{Color.FAIL}invalid input{Color.FAIL}")
        start = input("Start date ? ")
        end = input("End date ? ")
        desc = input("Description ? ")
        TournamentManager.create_tournament(
            {
                'name': name,
                'location': location,
                'rating': ratings[rating],
                'start': start,
                'end': end,
                'desc': desc,
            },
            self.dirname,
        )

    def add_player(self, tournament):
        print("+++++++ Add Player ++++++++")
        player = PlayerUI(self.dirname)
        while True:
            if len(tournament.players) >= 8:
                print(f"{Color.FAIL}This tournament is full{Color.ENDC}")
                index = None
                break
            players_ids = [x[0] for x in tournament.players]
            print(f"Registered players ids: {players_ids}")
            index = player.select()
            if index == -1:
                break
            if App.players[index].id not in players_ids:
                TournamentManager.add_player(index, tournament, self.dirname)
                print(f"{Color.OKGREEN}{App.players[index]} successfully registered to the tournament{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            else:
                print(f"{Color.FAIL}{App.players[index]} is already registered to the tournament{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
        return index
