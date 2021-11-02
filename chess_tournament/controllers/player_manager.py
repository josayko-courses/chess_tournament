"""Player Manager

"""

from controllers import App
from models import Player, Database


class PlayerManager:
    def create_error(surname, name, rank):
        if len(surname) < 2:
            return "surname input must be more than 1 character"
        elif len(name) < 2:
            return "name input must be more than 1 character"
        try:
            rank = int(rank)
            if rank <= 0:
                return "rank input is invalid"
        except ValueError:
            return "rank input is invalid"
        return None

    def create_player(input, dirname):
        new_player = Player(
            0,
            input['surname'],
            input['name'],
            input['birthdate'],
            input['gender'],
            input['rank'],
        )
        new_player.id = new_player.save_player_to_db(dirname)
        App.players.append(new_player)
        return

    def update_rank(id, new_rank, dirname):
        db = Database(dirname)
        # Add to db
        db.players.update({'rank': new_rank}, doc_ids=[id])
