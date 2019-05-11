from flask import Flask , json
from flask import jsonify
from flask_cors import CORS
from flask import send_file
import json
from io import BytesIO
import zipfile

app = Flask(__name__)
cors = CORS(app)



@app.route("/")
def hello():
    return "Hello World!"

@app.route('/json0', methods=['GET'])
def json0():
    with open('data.json') as test_file:
    	data = json.load(test_file)
    return jsonify(data)

@app.route('/SA3_2016_AUST.zip', methods=['GET','POST'])
def zip1():
    return send_file('SA3_2016_AUST.zip', attachment_filename='capsule.zip', as_attachment=True)


@app.route('/json1', methods=['GET'])
def json1():
    with open('Aurin.json') as aurin_file:
    	data = json.load(aurin_file)
    return jsonify(data)

@app.route('/json2', methods=['GET'])
def json2():
    with open('data1.json') as tweet_file:
        data = json.load(tweet_file)
    return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True)