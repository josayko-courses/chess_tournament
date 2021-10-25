"""Player Manager

"""

from controllers import App
from models import Player, Database


class PlayerManager:
    def create(input, dirname):
        db = Database(dirname)

        # Add to db
        id = db.create_player(input)
        new_player = Player(
            id,
            input['surname'],
            input['name'],
            input['birthdate'],
            input['gender'],
            input['rank'],
        )
        App.players.append(new_player)
        return

    def update_rank(id, new_rank, dirname):
        db = Database(dirname)
        # Add to db
        db.players.update({'rank': new_rank}, doc_ids=[id])
