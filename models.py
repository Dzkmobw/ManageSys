from extension import db

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    player_number = db.Column(db.String(255),nullable = False)
    player_name = db.Column(db.String(255),nullable = False)
    player_age = db.Column(db.String(255))
    player_position = db.Column(db.String(255),nullable = False)
    goals = db.Column(db.String(255))
    assists = db.Column(db.String(255))

        #初始化数据库
@staticmethod
def init_db():
    rets = [
        (1,'21','安东尼·马特乌斯·多斯·桑托斯',21,'LeftBack',114,514),
        ]
    for ret in rets:
        player = Player()
        player.id = ret[0]
        player.player_number = ret[1]
        player.player_name = ret[2]
        player.player_age = ret[3]
        player.player_position = ret[4]
        player.goals = ret[5]
        player.assists = ret[6]
        db.session.add(player)
    db.session.commit()