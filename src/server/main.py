from flask import Flask
from flask import jsonify

from ..utils.recomendations import Recomendations

app = Flask(__name__)

__recomendations = Recomendations()

@app.route('/v1/recomendations', methods=['GET'])
def get_recomendations():
    response = {
      'success': True,
      'items': __recomendations.get_recomendations()
    }
    return jsonify(response)

@app.route('/v1/recomendations/<songId>', methods=['GET'])
def get_recomendations_by_songid(songId):
    response = {
      'success': True,
      'items': __recomendations.get_recomendations_by_songId(songId)
    }
    return jsonify(response)