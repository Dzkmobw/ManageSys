from extension import db

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_number = db.Column(db.String(255), nullable=False)
    player_name = db.Column(db.String(255), nullable=False)
    player_age = db.Column(db.Integer)
    player_position = db.Column(db.String(255), nullable=False)
    player_goals = db.Column(db.Integer)
    player_assists = db.Column(db.Integer)

#初始化数据库
    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, '21', '安东尼·马特乌斯·多斯·桑托斯', 21, 'LeftBack', 114, 514),
            (2, '15', '尼古拉斯·杰克逊', 22, 'ST', 0, 0),

        ]
        for ret in rets:
            player = Player()
            player.id = ret[0]
            player.player_number = ret[1]
            player.player_name = ret[2]
            player.player_age = ret[3]
            player.player_position = ret[4]
            player.player_goals = ret[5]
            player.player_assists = ret[6]
            db.session.add(player)
        db.session.commit()
