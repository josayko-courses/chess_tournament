"""Player Manager

"""

from controllers import App
from models import Player, Database


class PlayerManager:
    def create(input, dirname):
        print("create_player")
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
