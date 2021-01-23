from flask import Flask, jsonify, request 
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__) 
CORS(app)

ma = Marshmallow(app)

# classes
class Car():
    def __init__(self, name, carType, carRange, cost, seats, saving, link):
        self.name = name
        self.carType = carType
        self.carRange = carRange
        self.cost = cost
        self.seats = seats
        self.saving = saving
        self.link = link

class CarSchema(ma.Schema):
    class Meta:
        fields = ('name', 'carType', 'carRange', 'cost', 'seats', 'saving', 'link')

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
    saving = carList[5]
    link = carList[6]
    car = Car(name, carType, carRange, cost, seats, saving, link)
    return car

@app.route('/', methods = ['GET', 'POST']) 
def home():
  data_file = open("vehicles.txt", "r")
  return parse_car_data()

@app.route('/output', methods = ['GET', 'POST'])
def output():
  # 1. receive input from user (will fake for now)    
    cost = 40000 # consider range
    location = 'New Brunswick' # province
    kperYear = 40000 #(high, med, low) -> high 
    numSeats = 5 # consider range

    trueList = list_of_cars

    # reducing cost based on savings
    for i in trueList:
        i.cost = int(i.cost) - int(i.saving)

    if cost < 43000:
        for i in trueList:
            if i.cost >= 43000:
                trueList.remove(i)

    #return 5


# driver function 
if __name__ == '__main__': 
	app.run(debug = True) 
