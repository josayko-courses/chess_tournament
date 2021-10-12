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
            half = int(len(players) / 2)
            first_players = rank_list[:half]
            second_players = rank_list[half:]
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
                self.swiss_round_algo(Tournament.t_list[select])
            else:
                return error_msg('The actual round is not marked as finish')
        else:
            return error_msg('Maximum number of rounds reached')

        input("Press ENTER to continue...\n")

    def swiss_round_algo(self, tournament):
        print('Swiss round algo')

        # Sort players by score and rank
        players = [p for p in tournament.players]
        sorted_players = sorted(players, key=lambda x: x[1], reverse=True)

        # bubble sort: if scores are equals, sort by rank (ascending)
        i = 1
        while i < len(sorted_players):
            if sorted_players[i][1] == sorted_players[i - 1][1]:
                if sorted_players[i][0].rank < sorted_players[i - 1][0].rank:
                    sorted_players[i], sorted_players[i - 1] = sorted_players[i - 1], sorted_players[i]
                    i = 1
                    continue
            i += 1

        # Get all previous games combinations
        l_rounds = tournament.rounds
        combos = []
        for r in l_rounds:
            for g in r.games:
                combos.append([g[0][0].id, g[1][0].id])

        # Create pairs
        p_ids = [x[0].id for x in sorted_players]
        id_games = []
        while len(p_ids) >= 2:
            p1 = p_ids[0]
            i = 1
            while i < len(p_ids):
                p2 = p_ids[i]
                if p1 != p2 and [p1, p2] not in combos and [p2, p1] not in combos:
                    id_games.append([p1, p2])
                    p_ids.remove(p1)
                    p_ids.remove(p2)
                    break
                i += 1

        l_pair = []
        db_pair = []
        for pair in id_games:
            p1 = [x for x in sorted_players if x[0].id == pair[0]]
            p2 = [x for x in sorted_players if x[0].id == pair[1]]
            l_pair.append(([p1[0][0], 0], [p2[0][0], 0]))
            db_pair.append(([pair[0], 0], [pair[1], 0]))

        nb = len(tournament.rounds) + 1
        round = Round(f"Round {nb}", l_pair)
        tournament.rounds.append(round)

        # DB
        table = self.tm.table
        db_tournament = table.get(doc_id=tournament.id)
        r_list = db_tournament['rounds']

        serialized_round = {'name': round.name, 'start': round.start, 'end': round.end, 'games': db_pair}
        r_list.append(serialized_round)

        table.update(
            {'rounds': r_list},
            doc_ids=[tournament.id],
        )

    def terminate_round(self):
        print("+ Terminate round +")
        select = select_tournament()

        if select == None:
            return

        if not Tournament.t_list[select].rounds[-1].end:
            r_list = Tournament.t_list[select].rounds[-1]
            for game in r_list.games:
                if game[0][1] == 0 and game[1][1] == 0:
                    return error_msg("There are some games with no results. Please add results before.")
            r_list.end = datetime.today().strftime('%Y-%m-%d %H:%M')

            tournaments = self.tm.table
            for t in tournaments:
                if t.doc_id == Tournament.t_list[select].id:
                    rounds = t['rounds']

            r_list = []
            updated_round = {}
            for i, round in enumerate(rounds):
                if i == len(rounds) - 1:
                    updated_round['name'] = round['name']
                    updated_round['start'] = round['start']
                    updated_round['end'] = datetime.today().strftime('%Y-%m-%d %H:%M')
                    updated_round['games'] = round['games']
                    r_list.append(updated_round)
                else:
                    r_list.append(round)

            tournaments.update(
                {'rounds': r_list},
                doc_ids=[Tournament.t_list[select].id],
            )

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

        r_index = input("Enter round number: ")
        try:
            r_index = int(r_index) - 1
            if r_index < 0 or r_index >= len(rounds):
                return error_msg("invalid input")
        except ValueError:
            return error_msg("invalid input")

        print(f"Name: {rounds[r_index].name}")
        print(f"Start: {rounds[r_index].start}")
        if rounds[r_index].end:
            print(f"End: {rounds[r_index].end}")
        else:
            print(f"End: ~ ONGOING ~")
        for i, game in enumerate(rounds[r_index].games):
            print(
                f"    [{i + 1}] {game[0][0].surname}, {game[0][0].name} <rank: {game[0][0].rank}, score: {game[0][1]}> ",
                end="",
            )
            print(f"vs. {game[1][0].surname}, {game[1][0].name}, <rank: {game[1][0].rank}, score: {game[1][1]}>")

        nb = input("    Enter game number: ")
        try:
            nb = int(nb) - 1
            if nb < 0 or nb >= len(rounds[r_index].games):
                return error_msg("invalid input")
        except ValueError:
            return error_msg("invalid input")

        game = rounds[r_index].games[nb]
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

        self.edit_scores(result, rounds[r_index].games[nb], select, r_index, nb)

        input("Press ENTER to continue...\n")

    def edit_scores(self, result, game, select, r_index, nb):
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
        for t in table:
            if t.doc_id == Tournament.t_list[select].id:
                tournament = t
        games = tournament['rounds'][r_index]['games']
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
            if i == r_index:
                serialized_round = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'games': serialized_games}
            else:
                serialized_round = r
            r_list.append(serialized_round)

        table.update(
            {'rounds': r_list},
            doc_ids=[Tournament.t_list[select].id],
        )
