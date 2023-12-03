import os
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd

import getActiveFireMap
import getDailyData
import getMLPrediction
import createFireMap
app = Flask(__name__)
cors = CORS(app)


@app.route('/historical_fire', methods=['POST'])
def receive_date():
    data = request.get_json()
    selected_date = data.get('selectedDate')
    getFireMap = getActiveFireMap.getFireMap(selected_date)
    map_html = getFireMap._repr_html_()
    return render_template_string('{{ map_html|safe }}', map_html=map_html), 200, {'Content-Type': 'text/html'}


@app.route('/')
def mauiWildfire():
    getDailyData
    prediction  = getMLPrediction.getPrediction()
    map_maui = createFireMap.getFireMap(prediction)
    map_html = map_maui._repr_html_()
    return render_template_string('{{ map_html|safe }}', map_html=map_html), 200, {'Content-Type': 'text/html'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))