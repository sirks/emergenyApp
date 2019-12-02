import json

from flask import Flask
from flask import request
from flask_cors import CORS

from python.UserEmePolygons import userdanger

app = Flask(__name__)

CORS(app)


@app.route('/api/polygons/', methods=['GET'])
def polygons():
    x = float(request.args.get('lat'))
    y = float(request.args.get('lon'))
    polygon = userdanger((x, y), 2222)

    return json.dumps(polygon)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
