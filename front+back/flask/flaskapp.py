from flask import Flask , json
from flask import jsonify
from flask_cors import CORS
import json
from io import BytesIO
import zipfile
import operator
from flask import send_file


app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/json0', methods=['GET'])
def json0():
    with open('Aurin.json') as aurin_file:
    	aurin_data = json.load(aurin_file)
    with open('pop.json') as pop_file:
        data1 = json.load(pop_file)
    data = []
    for row in aurin_data['features']:
        list1 = {}
        list1['sa3_code16'] = row['properties']['sa3_code16']
        list1['median_tot_prsnl_inc_weekly'] = row['properties']['median_tot_prsnl_inc_weekly']
        list1['median_age_persons'] = row['properties']['median_age_persons']
        for m in data1:
            if int(row['properties']['sa3_code16']) == m['SA3_CODE']:
                    list1['population'] = m['population']
                    data.append(list1)
    data.sort(key=operator.itemgetter('median_tot_prsnl_inc_weekly'))
    return jsonify(data)

@app.route('/geo1', methods=['GET'])
def geo1():
    with open('SA3_2016_AUST.json') as geo_file:
        data = json.load(geo_file)
    return jsonify(data)

@app.route('/geo2', methods=['GET'])
def geo2():
    with open('LGA_2016_AUST.json') as geo_file:
        data = json.load(geo_file)
    return jsonify(data)

@app.route('/lga', methods=['GET'])
def lga():
    with open('LGA.json') as geo_file:
        data = json.load(geo_file)
    return jsonify(data)


@app.route('/json1', methods=['GET'])
def json1():
    with open('Aurin.json') as aurin_file:
    	data = json.load(aurin_file)
    with open('pop.json') as pop_file:
        data1 = json.load(pop_file)
    for n in data['features']:
        for m in data1:
            if int(n['properties']['sa3_code16']) == m['SA3_CODE']:
                    n['properties']['population'] = m['population']

    return jsonify(data)

@app.route('/json2', methods=['GET'])
def json2():
    with open('data1.json') as tweet_file:
        data = json.load(tweet_file)
    return jsonify(data)

@app.route('/json3', methods=['GET'])
def json3():
    with open('chart.json') as text:
        data = json.load(text)
    data.sort(key=operator.itemgetter('median_tot_prsnl_inc_weekly'))
    return jsonify(data)

@app.route('/json4', methods=['GET'])
def json4():
    with open('brothel.json') as text:
        data = json.load(text)
    return jsonify(data)

@app.route('/image')
def get_image():
    filename = 'house.svg'
    return send_file(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="443")