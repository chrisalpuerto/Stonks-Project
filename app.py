from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import datetime
from downloader import download

app = Flask(__name__)

def load_data(symbol, start_date, end_date):
    try:
        with open('history.json', 'r') as f:
            data = json.load(f)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df[(df.index >= start_date) & (df.index <= end_date)]

        return df
    except FileNotFoundError:
        return None

@app.route('/download', methods=['GET'])



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        download(symbol, start_date, end_date)

        df = load_data(symbol, start_date, end_date)

        if df is not None:
            graph_json = df[['Close']].reset_index().to_json(orient='records')
            return jsonify({'graph_data': graph_json})
        else:
            return jsonify({'error': 'No data found.'}), 404

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)