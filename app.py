from flask import Flask, jsonify, request 
from flask_cors import CORS
import os
app = Flask(__name__) 
CORS(app)


@app.route('/', methods = ['GET', 'POST']) 
def home():
  data_file = open("SJ.txt", "r")
  return jsonify(data_file.readlines()[4::])

# driver function 
if __name__ == '__main__': 
	app.run(debug = True) 
