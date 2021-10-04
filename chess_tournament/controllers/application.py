"""Get tournament initialization details from User

"""

from controllers import TinyDB
from .tournament_manager import TournamentManager
from .menu_manager import MenuManager
from .player_manager import PlayerManager
from models import Round, Tournament, Player


class Application:
    def __init__(self, dirname):
        self.db_path = dirname + '/db.json'
        self.tm = TournamentManager(self.db_path)
        self.pm = PlayerManager(self.db_path)
        self.mm = MenuManager

    def load_db(self):
        db = TinyDB(self.db_path)
        tournaments = db.table('tournaments')
        for t in tournaments.all():
            tournament = Tournament(t['name'], t['location'], t['rating'], t['start'], t['end'], t['desc'])
            Tournament.t_list.append(tournament)

        players = db.table('players')
        for p in players.all():
            player = Player(p['surname'], p['name'], p['birthdate'], p['gender'], p['rank'])
            Player.p_list.append(player)

    def generate_round(players):
        new_round = Round()
        first_players = [p for i, p in enumerate(players) if i % 2 != 0]
        second_players = [p for i, p in enumerate(players) if i % 2 == 0]
        paired_players = zip(first_players, second_players)

        for p1, p2 in list(paired_players):
            new_round.create_game(p1, p2)

        print("Round created with the following games: ")
        for game in new_round.games:
            print(game)

        input("Press ENTER to continue...\n")
