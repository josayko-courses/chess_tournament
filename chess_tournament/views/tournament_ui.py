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
            error = TournamentManager.select_tournament_error(index)
            if error:
                continue
            else:
                return int(index) - 1

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
            player.create_player,
            self.add_player,
            self.tournament_report,
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
            print("[6] Tournament Report")
            print("[9] Main Menu")
            print("[0] Exit")
            select = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            error = TournamentManager.menu_error(select)
            if error:
                continue
            select = int(select)
            if select == 0:
                sys.exit(0)
            elif select == 9:
                return
            elif select > 0 and select < 7:
                if options[select](t) is None:
                    input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")

    def create(self):
        """Create a new tournament"""
        while True:
            print("+++++++ Create Tournament ++++++++")
            ratings = ("rapid", "blitz", "bullet")
            name = input("Name ? ")
            location = input("Location ? ")
            rating = input("Rating type :\n    [1] rapid\n    [2] blitz\n    [3] bullet\n    Rating ? ")
            start = input("Start date ? ")
            end = input("End date ? ")
            desc = input("Description ? ")
            error = TournamentManager.create_error(name, location, rating)
            if error:
                print(f"{Color.FAIL}{error}{Color.ENDC}")
                continue
            else:
                break

        TournamentManager.create_tournament(
            {
                "name": name,
                "location": location,
                "rating": ratings[int(rating) - 1],
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
        """Add a player to the tournament"""
        if tournament.rounds:
            print(f"{Color.FAIL}Cannot register player: tournament already started{Color.ENDC}")
            return None
        while True:
            print("+++++++ Add Player ++++++++")
            if TournamentManager.is_full(tournament):
                index = None
                break
            elif PlayerManager.no_players():
                return print(f"{Color.FAIL}No players{Color.ENDC}")
            print(f"Registered players ids: {tournament.get_players_ids()}")
            index = PlayerUI.select_player()
            if index == -1:
                break
            error = TournamentManager.add_player_check(index, tournament)
            if error:
                print(f"{Color.FAIL}{error}{Color.ENDC}")
                input(f"{Color.OKBLUE}Press ENTER to continue...{Color.ENDC}")
            else:
                TournamentManager.add_player(index, tournament, self.dirname)
                print(f"{Color.OKGREEN}{App.players[index]} successfully registered to the tournament{Color.ENDC}")
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

    def tournament_report(self, t):
        print(f"{Color.WARNING}+++++++ Tournament report ++++++++{Color.ENDC}")
        print(f"{Color.HEADER}| {t.id}. {t.name}, {t.location}, rating: {t.rating}, ", end="")
        print(f"dates: {t.start} - {t.end} |{Color.ENDC}")
        print(f"\"{t.desc}\"")
        print(f"{Color.BOLD}+ Players by rank +{Color.ENDC}")
        PlayerUI.print_players_by_rank(t.get_players_instance(App.players))

        print(f"{Color.BOLD}+ Players by name +{Color.ENDC}")
        PlayerUI.print_players_by_name(t.get_players_instance(App.players))

        print(f"{Color.BOLD}+ Players leaderboard +{Color.ENDC}")
        TournamentUI.print_leaderboard(t)

        print(f"{Color.BOLD}+ Rounds +{Color.ENDC}")
        RoundUI.print_rounds(t.rounds)
        print()
