"""Tournament information

"""

from .round import Round
from tinydb import TinyDB


class Tournament:
    def __init__(self, id, name, location, rating, desc, start, end=None):
        self.id = id
        self.name = name
        self.location = location
        self.rating = rating

        self.nb_rounds = 4
        self.rounds = []
        self.players = []

        self.start = start
        if end is None:
            self.end = start
        else:
            self.end = end

        self.desc = desc

    def deserialize(t):
        inst = Tournament(t.doc_id, t['name'], t['location'], t['rating'], t['desc'], t['start'], t['end'])

        for r in t['rounds']:
            round = Round(r['name'], r['games'], r['start'], r['end'])
            inst.rounds.append(round)
        inst.players = t['players']
        return inst

    def get_players_ids(self):
        return [x[0] for x in self.players]

    def get_players_instance(self, all_players):
        """Get players instance from ids"""
        players_ids = [x[0] for x in self.players]
        players = []
        for id in players_ids:
            for p in all_players:
                if p.id == id:
                    players.append(p)
        return players

    def get_players_with_score(self, all_players):
        """Get players instance and their score"""
        players = self.get_players_instance(all_players)
        scores = []
        for p_inst in players:
            for p_lst in self.players:
                if p_lst[0] == p_inst.id:
                    score = [p_inst, p_lst[1]]
                    scores.append(score)
        return scores

    def __repr__(self) -> str:
        str1 = f"Tournament(id={self.id}, name={self.name}, location={self.location}, rating={self.rating}, "
        str2 = f"desc={self.desc}, start={self.start}, end={self.end})"
        return str1 + str2

    def save_tournament_to_db(self, dirname):
        """save tournament to db"""
        db = TinyDB(dirname + '/db.json')
        tournaments_table = db.table('tournaments')
        new_tournament = {
            'name': self.name,
            'location': self.location,
            'rating': self.rating,
            'nb_rounds': self.nb_rounds,
            'rounds': self.rounds,
            'players': self.players,
            'start': self.start,
            'end': self.end,
            'desc': self.desc,
        }
        return tournaments_table.insert(new_tournament)

    def update_tournament_players_db(self, player, tournament_id, dirname):
        """Add updated players of tournament to db"""
        db = TinyDB(dirname + '/db.json')
        tournaments_table = db.table('tournaments')
        for t in tournaments_table:
            if t.doc_id == tournament_id:
                t['players'].append(player)
                tournaments_table.update(t, doc_ids=[tournament_id])

    def update_tournament_rounds_db(self, round, tournament_id, dirname):
        """Add updated rounds to db"""
        db = TinyDB(dirname + '/db.json')
        tournaments_table = db.table('tournaments')
        for t in tournaments_table:
            if t.doc_id == tournament_id:
                t['rounds'].append(round)
                tournaments_table.update(t, doc_ids=[tournament_id])

    def update_tournament_results_db(self, game, game_index, player1, player2, dirname):
        """Add updated game results in db"""
        db = TinyDB(dirname + '/db.json')
        tournaments_table = db.table('tournaments')
        for t in tournaments_table:
            if t.doc_id == self.id:
                break

        # Edit game
        updated_games = []
        for i, g in enumerate(t['rounds'][-1]['games']):
            if i == game_index:
                updated_games.append(game)
            else:
                updated_games.append(g)

        # Edit round with updated game
        updated_rounds = []
        for i, r in enumerate(t['rounds']):
            if i == len(t['rounds']) - 1:
                serialized_round = {'name': r['name'], 'start': r['start'], 'end': r['end'], 'games': updated_games}
                updated_rounds.append(serialized_round)
            else:
                updated_rounds.append(r)

        # Edit players total score
        updated_players = []
        for p in t['players']:
            if p[0] == player1[0]:
                updated_players.append(player1)
            elif p[0] == player2[0]:
                updated_players.append(player2)
            else:
                updated_players.append(p)

        # Save to db
        tournaments_table.update(
            {'rounds': updated_rounds, 'players': updated_players},
            doc_ids=[self.id],
        )
        return
