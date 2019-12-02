import json

from flask import Flask
from flask import request
from flask_cors import CORS

from python.UserEmePolygons import userdanger

app = Flask(__name__)

CORS(app)

nearby_degrees = 0.5
sosses = {'xxx': [60, 25]}


@app.route('/api/polygons/', methods=['GET'])
def polygons():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    polygon = userdanger((lat, lon), 2222)
    return json.dumps(polygon)


@app.route('/api/sos/', methods=['GET'])
def new_sos():
    id = request.args.get('id')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    sosses[id] = [lat, lon]
    return ''


@app.route('/api/unsos/', methods=['GET'])
def unsos():
    id = request.args.get('id')
    sosses.pop(id, None)
    return ''


@app.route('/api/sosses/', methods=['GET'])
def get_sosses():
    sosses['xxx'][0] += 0.01

    my_id = request.args.get('id')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    nearby_sosses = {id: location for id, location in sosses.items() if nearby(lat, lon, *location) and id != my_id}

    return json.dumps(nearby_sosses)


def nearby(lat, lon, lat_other, lon_other):
    return (abs(lat - lat_other) ** 2 + abs(lon - lon_other) ** 2) ** 0.5 <= nearby_degrees


def start_rest():
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')


if __name__ == "__main__":
    start_rest()
