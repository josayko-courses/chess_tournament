"""Tournament related views

"""

import sys
from controllers import App, PlayerManager, TournamentManager
from bcolors import Color
from views import PlayerUI, RoundUI


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
        print("+++++++ Start tournament ++++++++")
        if tournament.rounds:
            return print(f"{Color.FAIL}Tournament had already started{Color.ENDC}")
        elif not tournament.players or len(tournament.players) % 2 != 0:
            return print(f"{Color.FAIL}Not enough players{Color.ENDC}")
        TournamentManager.create_first_round(tournament, self.dirname)
        print(f"{Color.OKGREEN}Tournament sucessfully started at {tournament.rounds[0].start}{Color.ENDC}")

        # Print games info
        players = tournament.get_players_instance(App.players)
        print(f"{Color.WARNING}Next games: ")
        for i, game in enumerate(tournament.rounds[0].games):
            for p in players:
                if game[0][0] == p.id:
                    p1 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}"
                if game[1][0] == p.id:
                    p2 = f"id: {p.id}, {p.surname} {p.name}, rank: {p.rank}"
            print(f"Game {i + 1} | {p1} vs. {p2}")
        print(f"{Color.ENDC}", end="")

    def menu(self, index):
        """Tournament menu"""
        t = App.tournaments[index]
        player = PlayerUI(self.dirname)
        round = RoundUI(self.dirname)

        options = [
            "Exit",
            round.edit,
            round.terminate,
            self.start,
            player.create,
            self.add_player,
        ]
        while True:
            print("\n+=== Tournament Menu ===+")
            print(f"{Color.HEADER}{t.name}, {t.location}, {t.rating}, {t.start}, {t.end}{Color.ENDC}")
            if t.rounds:
                ongoing_round = f"{t.rounds[-1].name}, start: {t.rounds[-1].start}, end: {t.rounds[-1].end}"
            else:
                ongoing_round = "Not Started"
            print(f"{Color.HEADER}{ongoing_round}{Color.ENDC}")
            print("+=======================+")
            print("[1] Edit Round")
            print("[2] Terminate Round")
            print("[3] Start Tournament")
            print("[4] Create Player")
            print("[5] Add Player")
            print("[9] Main Menu")
            print("[0] Exit")
            select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            try:
                select = int(select)
                if select == 0:
                    sys.exit(0)
                elif select == 9:
                    return
                elif select > 0 and select < 6:
                    if options[select](t) is None:
                        input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            except ValueError:
                continue

    def create(self):
        print("+++++++ Create Tournament ++++++++")
        ratings = ("rapid", "blitz", "bullet")
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
                "name": name,
                "location": location,
                "rating": ratings[rating],
                "start": start,
                "end": end,
                "desc": desc,
            },
            self.dirname,
        )
        print(f"{Color.OKGREEN}New tournament created{Color.ENDC}")
        input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
        return len(App.tournaments) - 1

    def add_player(self, tournament):
        print("+++++++ Add Player ++++++++")
        if tournament.rounds:
            print(f"{Color.FAIL}Cannot register player: tournament already started{Color.ENDC}")
            return None
        while True:
            if len(tournament.players) >= 8:
                print(f"{Color.FAIL}This tournament is full{Color.ENDC}")
                index = None
                break
            players_ids = [x[0] for x in tournament.players]
            if not App.players:
                return print(f"{Color.FAIL}No players{Color.ENDC}")
            print(f"Registered players ids: {players_ids}")
            index = PlayerUI.select()
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

    def print_leaderboard(tournament):
        players = tournament.get_players_with_score(App.players)
        sorted_players = sorted(players, key=lambda x: x[1], reverse=True)

        for i, p in enumerate(sorted_players):
            print(
                f"<{i + 1}> score: {p[1]} | id: {p[0].id} - {p[0].surname} {p[0].name}, ",
                end="",
            )
            print(f"{p[0].birthdate}, {p[0].gender} - rank: {p[0].rank}")
        return

    def edit_player_rank(self):
        print(f"{Color.WARNING}+++++++ Edit player rank ++++++++{Color.ENDC}")
        if not App.players:
            return print(f"{Color.FAIL}No players{Color.ENDC}")
        index = PlayerUI.select()
        if index == -1:
            return -1

        player = App.players[index]
        print(f"    /* Edit {player.surname} {player.name}, rank: {player.rank} */")
        old_rank = player.rank

        new_rank = input("New rank ? ")
        try:
            new_rank = int(new_rank)
            player.rank = new_rank
            print(f"    {player.surname} {player.name}, rank: {old_rank} => rank: {new_rank}")
        except ValueError:
            return print(f"{Color.FAIL}Error: invalid input{Color.ENDC}")

        PlayerManager.update_rank(player.id, new_rank, self.dirname)
        return
