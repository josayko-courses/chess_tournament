"""Get tournament initialization details from User

"""

from controllers import TinyDB
from .tournament_manager import TournamentManager
from .menu_manager import MenuManager
from .player_manager import PlayerManager
from models import Tournament, Player
from views import error_msg, select_tournament
from models import Tournament, Round


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

        # next rounds

        input("Press ENTER to continue...\n")
