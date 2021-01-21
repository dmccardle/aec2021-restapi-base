from flask import Flask, jsonify, request 
import os
app = Flask(__name__) 


@app.route('/', methods = ['GET', 'POST']) 
def home():
  data_file = open("SJ.txt", "r")
  return(data_file.readlines()[0])

# driver function 
if __name__ == '__main__': 
	app.run(debug = True) 
