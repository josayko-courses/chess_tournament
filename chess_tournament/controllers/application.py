"""Get tournament initialization details from User

"""

from controllers import TinyDB
from .tournament_manager import TournamentManager
from .menu_manager import MenuManager
from .player_manager import PlayerManager
from models import Tournament, Player
from views import error_msg, select_tournament
from models import Tournament, Round
from datetime import datetime


class Application:
    def __init__(self, dirname):
        self.db_path = dirname + '/db.json'
        self.tm = TournamentManager(self.db_path)
        self.pm = PlayerManager(self.db_path)
        self.mm = MenuManager

    def load_db(self):
        db = TinyDB(self.db_path)
        players = db.table('players')
        for p in players.all():
            player = Player(p.doc_id, p['surname'], p['name'], p['birthdate'], p['gender'], p['rank'])
            Player.p_list.append(player)

        tournaments = db.table('tournaments')

        # Loading tournaments
        for t in tournaments.all():
            tournament = Tournament(t.doc_id, t['name'], t['location'], t['rating'], t['start'], t['end'], t['desc'])

            # Loading players and scores in each tournament => [<Player>, score]
            for p in t['players']:
                player = [x for x in Player.p_list if x.id == p[0]]
                player.append(p[1])
                tournament.players.append(player)
            Tournament.t_list.append(tournament)

            # Loading rounds and games
            for r in t['rounds']:
                deserialized_games = []
                for g in r['games']:
                    p1 = [x for x in Player.p_list if x.id == g[0][0]]
                    p1.append(g[0][1])
                    p2 = [x for x in Player.p_list if x.id == g[1][0]]
                    p2.append(g[1][1])
                    deserialized_games.append((p1, p2))

                deserialized_round = Round(r['name'], deserialized_games, r['start'], r['end'])
                tournament.rounds.append(deserialized_round)

    def generate_round(self):
        select = select_tournament()
        if select == None:
            return

        # First round
        if len(Tournament.t_list[select].rounds) == 0:
            players = [p for p in Tournament.t_list[select].players]
            rank_list = sorted(players, key=lambda x: x[0].rank)

            # Create pairs
            first_players = rank_list[:4]
            second_players = rank_list[4:]
            paired_players = zip(first_players, second_players)

            games = [g for g in paired_players]
            round = Round("Round 1", games)
            Tournament.t_list[select].rounds.append(round)

            # Update DB
            table = self.tm.table
            tournament = table.get(doc_id=Tournament.t_list[select].id)
            r_list = tournament['rounds']

            serialized_games = []
            for game in games:
                player1 = [game[0][0].id, game[0][1]]
                player2 = [game[1][0].id, game[1][1]]
                serialized_games.append((player1, player2))

            serialized_round = {'name': round.name, 'start': round.start, 'end': round.end, 'games': serialized_games}
            r_list.append(serialized_round)

            table.update(
                {'rounds': r_list},
                doc_ids=[Tournament.t_list[select].id],
            )

        # next rounds
        elif len(Tournament.t_list[select].rounds) < Tournament.t_list[select].nb_rounds:
            if Tournament.t_list[select].rounds[-1].end:
                self.swiss_round_algo()
            else:
                print('The actual round is not marked as finish')

        input("Press ENTER to continue...\n")

    def swiss_round_algo(self):
        print('Round finished: ok')
        input("Press ENTER to continue...\n")

    def terminate_round(self):
        print("+ Terminate round +")
        select = select_tournament()

        if not Tournament.t_list[select].rounds[-1].end:
            r_list = Tournament.t_list[select].rounds[-1]
            for game in r_list.games:
                if game[0][1] == 0 and game[1][1] == 0:
                    return error_msg("There are some games with no results. Please add results before.")
            r_list.end = datetime.today().strftime('%Y-%m-%d %H:%M')
        else:
            return error_msg("There is no ongoing round.")

        input("Press ENTER to continue...\n")

    def add_results(self):
        print("+ Add results +")
        select = select_tournament()
        if select == None:
            return

        rounds = Tournament.t_list[select].rounds
        for index, round in enumerate(rounds):
            if round.end:
                print(f"    [{index + 1}] {round.name}, {round.start}, {round.end}")
            else:
                print(f"    [{index + 1}] {round.name}, {round.start} ~ ONGOING ~")

        select = input("Enter round number: ")
        try:
            select = int(select) - 1
            if select < 0 or select >= len(rounds):
                return error_msg("invalid input")
        except ValueError:
            return error_msg("invalid input")

        print(f"Name: {rounds[select].name}")
        print(f"Start: {rounds[select].start}")
        if rounds[select].end:
            print(f"End: {rounds[select].end}")
        else:
            print(f"End: ~ ONGOING ~")
        for i, game in enumerate(rounds[select].games):
            print(
                f"    [{i + 1}] {game[0][0].surname}, {game[0][0].name} <rank: {game[0][0].rank}, score: {game[0][1]}> ",
                end="",
            )
            print(f"vs. {game[1][0].surname}, {game[1][0].name}, <rank: {game[1][0].rank}, score: {game[1][1]}>")

        nb = input("    Enter game number: ")
        try:
            nb = int(nb) - 1
            if nb < 0 or nb >= len(rounds[select].games):
                return error_msg("invalid input")
        except ValueError:
            return error_msg("invalid input")

        game = rounds[select].games[nb]
        print(
            f"        >> {game[0][0].surname}, {game[0][0].name} <rank: {game[0][0].rank}, score: {game[0][1]}> ",
            end="",
        )
        print(f"vs. {game[1][0].surname}, {game[1][0].name}, <rank: {game[1][0].rank}, score: {game[1][1]}>")

        print(f"        [1] +1, +0")
        print(f"        [2] +0, +1")
        print(f"        [3] +0.5, +0.5")
        print(f"        [4] -1, -0")
        print(f"        [5] -0, -1")
        print(f"        [6] -0.5, -0.5")
        result = input("        Select result: ")

        try:
            result = int(result) - 1
            if result < 0 or result > 5:
                return error_msg("invalid input")
        except ValueError:
            return error_msg("invalid input")

        self.edit_scores(result, rounds[select].games[nb], select, nb)

        input("Press ENTER to continue...\n")

    def edit_scores(self, result, game, select, nb):
        if result == 0:
            game[0][1] += 1
        if result == 1:
            game[1][1] += 1
        if result == 2:
            game[0][1] += 0.5
            game[1][1] += 0.5
        if result == 3:
            game[0][1] -= 1
        if result == 4:
            game[1][1] -= 1
        if result == 5:
            game[0][1] -= 0.5
            game[1][1] -= 0.5

        print(
            f"        >> {game[0][0].surname}, {game[0][0].name} <rank: {game[0][0].rank}, score: {game[0][1]}> ",
            end="",
        )
        print(f"vs. {game[1][0].surname}, {game[1][0].name}, <rank: {game[1][0].rank}, score: {game[1][1]}>")

        # Update DB
        table = self.tm.table
        tournament = table.get(doc_id=Tournament.t_list[select].id)
        games = tournament['rounds'][select]['games']
        serialized_games = []
        for i, g in enumerate(games):
            if i == nb:
                player1 = [g[0][0], game[0][1]]
                player2 = [g[1][0], game[1][1]]
                self.pm.edit_players_score(tournament, Tournament.t_list[select], [player1, player2], result)
            else:
                player1 = [g[0][0], g[0][1]]
                player2 = [g[1][0], g[1][1]]
            serialized_games.append((player1, player2))

        r_list = []
        for i, r in enumerate(tournament['rounds']):
            if i == select:
                serialized_round = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'games': serialized_games}
            else:
                serialized_round = r
            r_list.append(serialized_round)

        # table.update(
        #     {'rounds': r_list},
        #     doc_ids=[Tournament.t_list[select].id],
        # )
