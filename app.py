from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('nbaplayer', user='frankie', password='123', host='localhost', port='5432')

class BaseModel(Model):
  class Meta:
    database = db

class NbaPlayer(BaseModel):
  name = CharField()
  age = IntegerField()
  height = CharField()
  position = CharField()

db.connect()
db.drop_tables([NbaPlayer])
db.create_tables([NbaPlayer])


NbaPlayer(name='Lebron James', age='38', height='6ft 9in', position='small forward').save()
NbaPlayer(name='Jimmy Butler', age='33', height='6ft 7in', position='small forward').save()
NbaPlayer(name='Jalen Brunson', age='26', height='6ft 2in', position='point guard').save()
NbaPlayer(name='Devin Booker', age='26', height='6ft 5in', position='shooting guard').save()


app = Flask(__name__)

@app.route('/players/', methods=['GET', 'POST'])
@app.route('/players/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(NbaPlayer.get(NbaPlayer.id == id)))
    else:
        NbaPlayers_list = []
        for player in NbaPlayer.select():
            NbaPlayers_list.append(model_to_dict(player))
        return jsonify(NbaPlayers_list)

  if request.method =='PUT':
    body = request.get_json()
    player.update(body).where(player.id == id).execute()
    return f'{id} has been updated.'

  if request.method == 'POST':
    new_player = dict_to_model(player, request.get_json())
    new_player.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    player.delete().where(player.id == id).execute()
    return f'{id} deleted.'

app.run(debug=True, port=5000)