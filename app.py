from flask import Flask, jsonify, request 
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__) 
CORS(app)

ma = Marshmallow(app)

# classes
class Car():
    def __init__(self, name, carType, carRange, cost, seats, link):
        self.name = name
        self.carType = carType
        self.carRange = carRange
        self.cost = cost
        self.seats = seats
        self.link = link

class CarSchema(ma.Schema):
    class Meta:
        fields = ('name', 'carType', 'carRange', 'cost', 'seats', 'link')

list_of_cars = []
car_schema = CarSchema(many=True)

# does parsing
def parse_car_data():
    data_file = open("vehicles.txt", "r")
    Lines = data_file.readlines()
    for i in range(2, len(Lines)):
        car = parse_car_from_data_lines(Lines[i])
        list_of_cars.append(car)
    return car_schema.jsonify(list_of_cars)

# builds and returns a City object based on the list of data provided
def parse_car_from_data_lines(car_data_lines):
    carList = car_data_lines.split(",")
    name = carList[0]
    carType = carList[1]
    carRange = carList[2]
    cost = carList[3]
    seats = carList[4]
    link = carList[5]
    car = Car(name, carType, carRange, cost, seats, link)
    return car

@app.route('/', methods = ['GET', 'POST']) 
def home():
  data_file = open("vehicles.txt", "r")
  return parse_car_data()

#@app.route('/', methods = ['GET', 'POST']) 
#def home():
  # 1. receive input from user (will fake for now)
   # data_file = open("vehicles.txt", "r")
    #parse_car_data()
    #for i in range(2, 11):
    #    print(list_of_cars[i])
    
    #cost = 40000 # consider range
    #location = 'New Brunswick' # province
    #kperYear = 40000 (high, med, low) # -> high
    #numSeats = 5 # consider range

    #return 5


# driver function 
if __name__ == '__main__': 
	app.run(debug = True) 
