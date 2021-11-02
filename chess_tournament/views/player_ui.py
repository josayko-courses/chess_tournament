"""Player related views

"""

from controllers import App, TournamentManager, PlayerManager
from bcolors import Color


class PlayerUI:
    def __init__(self, dirname):
        self.dirname = dirname

    def select_player():
        while True:
            print("+++++++ Select player ++++++++")
            for i, t in enumerate(App.players):
                print(f"[{i + 1}] {t}")
            print("[0] Cancel")
            index = input(f"{Color.BOLD}>>> Select: {Color.ENDC}")
            error = PlayerManager.select_player_error(index)
            if error:
                continue
            else:
                return int(index) - 1

    def create_player(self, tournament):
        while True:
            print("+++++++ Create player ++++++++")
            surname = input("Surname ? ")
            name = input("Name ? ")
            birthdate = input("Birth Date ? ")
            gender = input("Gender ? ")
            rank = input("Rank ? ")
            error = PlayerManager.create_error(surname, name, rank)
            if error:
                print(f"{Color.FAIL}{error}{Color.ENDC}")
                continue

            PlayerManager.create_player(
                {'surname': surname, 'name': name, 'birthdate': birthdate, 'gender': gender, 'rank': rank},
                self.dirname,
            )
            print(f"{Color.OKGREEN}New {App.players[-1]} has been created{Color.ENDC}")

            if len(tournament.players) < 8:
                index = len(App.players) - 1
                while True:
                    select = input("Add new Player to this tournament ? (y/n, default=y) ")
                    if select.capitalize() == 'N':
                        break
                    if tournament.rounds:
                        print(f"{Color.FAIL}Cannot register player: tournament already started{Color.ENDC}")
                        break
                    elif not select or select.capitalize() == 'Y':
                        TournamentManager.add_player(index, tournament, self.dirname)
                        print(f"{Color.OKGREEN}{App.players[index]} has been registered to the tournament{Color.ENDC}")
                        break
            cancel = input("Create another player ? (y/n, default=y) ")
            if cancel.capitalize() == 'N':
                return -1

    def print_players_by_rank(players):
        rank_list = sorted(players, key=lambda x: x.rank)
        for player in rank_list:
            print(f"id: {player.id}, name: {player.surname} {player.name}, ", end="")
            print(f"birthdate: {player.birthdate}, gender: {player.gender}, rank: {player.rank}")
        return

    def print_players_by_name(players):
        alpha_list = sorted(players, key=lambda x: x.surname + x.name)
        for player in alpha_list:
            print(f"id: {player.id}, name: {player.surname} {player.name}, ", end="")
            print(f"birthdate: {player.birthdate}, gender: {player.gender}, rank: {player.rank}")
