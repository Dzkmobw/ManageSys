from flask import request, json, Flask
from flask.views import MethodView
from extension import db,cors
from models import Player
from typing import List

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
db.init_app(app)
cors.init_app(app)

#终端输入flask create即可初始化数据库
@app.cli.command() # 自定义指令
def create():
    db.drop_all()   # 把旧的数据表全部删除
    db.create_all() # 创建一个新的数据表
    Player.init_db()  # 初始化数据


class PlayerApi(MethodView):
    def get(self,player_id):
        #获取球员信息
        # 如果没有指定ID，返回所有球员
        if not player_id:
            players: List[Player] = Player.query.all() # 类型注释，表示Players是一个列表，列表中的元素都是Player元素
            results = [
                {
                    'id':player.id,
                    'player_number':player.player_number,
                    'player_name':player.player_name,
                    'player_age':player.player_age,
                    'player_position':player.player_position,
                    'player_goals':player.player_goals,
                    'player_assists':player.player_assists,
                } for player in players
            ] # 列表推导式
            ret = {
                'status' : 'success',
                'message' : '数据查询成功',
                'results': results
            }
        else:
            player: Player = Player.query.get(player_id)
            ret= {
                'status': 'success',
                'message': '数据查询成功',
                'results': {
                    'id':player.id,
                    'player_number':player.player_number,
                    'player_name':player.player_name,
                    'player_age':player.player_age,
                    'player_position':player.player_position,
                    'player_goals':player.player_goals,
                    'player_assists':player.player_assists,
                }
            }
        # 返回中文
        return json.dumps(ret, ensure_ascii=False)

    def post(self):
        #新增球员
        form = request.json
        player = Player()
        player.player_number = form.get('player_number')
        player.player_name = form.get('player_name')
        player.player_age = form.get('player_age')
        player.player_position = form.get('player_position')
        player.player_goals = form.get('player_goals')
        player.player_assists = form.get('player_assists')
        db.session.add(player)
        db.session.commit()
        ret =  {
            'status': 'success',
            'message': '数据添加成功',
        }
        return json.dumps(ret, ensure_ascii=False)

    def delete(self,player_id):
        #删除球员
        player = Player.query.get(player_id)
        db.session.delete(player)
        db.session.commit()
        ret = {
            'status': 'success',
            'message': '数据删除成功',
        }
        return json.dumps(ret, ensure_ascii=False)

    def put(self,player_id):
        #数据库更新
        player:Player = Player.query.get(player_id)
        player.player_number = request.json.get('player_number')
        player.player_name = request.json.get('player_name')
        player.player_age = request.json.get('player_age')
        player.player_position = request.json.get('player_position')
        player.player_goals = request.json.get('player_goals')
        player.player_assists = request.json.get('player_assists')
        db.session.commit()
        ret =  {
            'status': 'success',
            'message': '数据修改成功',
        }
        return json.dumps(ret, ensure_ascii=False)

player_view = PlayerApi.as_view('player_api')

# 注意斜杠问题
@app.route('/')
def hello():
    return 'nihao'

app.add_url_rule('/players/', defaults={'player_id':None}, view_func=player_view,methods=['GET',])
app.add_url_rule('/players/', view_func=player_view, methods=['POST',])
app.add_url_rule('/players/<int:player_id>', view_func=player_view, methods=['GET','PUT','DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
