from flask import Flask
from flask import request
import json
from flask_cors import CORS
app = Flask(__name__)

CORS(app)


@app.route('/api/polygons/', methods=['GET'])
def polygons():
    x = request.args.get('lat')
    y = request.args.get('lon')
    print('Result: ', x, y)

    polygon = [[
            [
              11.865234375,
              56.607885465009254
            ],
            [
              12.216796875,
              56.46249048388979
            ],
            [
              9.052734375,
              55.677584411089526
            ],
            [
              13.974609375,
              55.02802211299252
            ],
            [
              14.326171874999998,
              56.36525013685606
            ],
            [
              11.865234375,
              56.607885465009254
            ]
          ],
               [
            [
              26.015625,
              59.355596110016315
            ],
            [
              30.585937499999996,
              62.2679226294176
            ],
            [
              24.960937499999996,
              63.39152174400882
            ],
            [
              21.09375,
              61.938950426660604
            ],
            [
              21.09375,
              57.51582286553883
            ],
            [
              26.015625,
              59.355596110016315
            ]
          ]]

    return str(polygon) # "{}{}".format(x,y)

def hello():
    return "Hello Kriss!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
