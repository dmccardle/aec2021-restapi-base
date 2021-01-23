from flask import Flask, jsonify, request 
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os
import json
app = Flask(__name__) 
CORS(app)

ma = Marshmallow(app)

# classes
class Car():
    def __init__(self, name, carType, carRange, cost, seats, saving, batterySize, link, costAnalysis, emissions):
        self.name = name
        self.carType = carType
        self.carRange = carRange
        self.cost = cost
        self.seats = seats
        self.saving = saving
        self.link = link
        self.batterySize = batterySize
        self.costAnalysis = costAnalysis
        self.emissions = emissions

class CarSchema(ma.Schema):
    class Meta:
        fields = ('name', 'carType', 'carRange', 'cost', 'seats', 'saving', 'batterySize', 'link', 'costAnalysis', 'emissions')

list_of_cars = []

# $/kWH
prov =	{
    "AB" : 16.7,
    "BC" : 12.4,
    "MB" : 9.6,
    "NB" : 12.7,
    "NL" : 13.8,
    "NS" : 15.0,
    "NT" : 38.7,
    "NU" : 37.5,
    "ON" : 12.5,
    "PE" : 16.8,
    "QC" : 7.3,
    "SK" : 18.2,
    "YT" : 14.5
}


gasCharge = 1 # $/litre
car_schema = CarSchema(many=True)

# does parsing
def parse_car_data():
    data_file = open("vehicles.txt", "r")
    Lines = data_file.readlines()
    for i in range(2, len(Lines)):
        car = parse_car_from_data_lines(Lines[i])
        list_of_cars.append(car)
    return car_schema.jsonify(list_of_cars)

# builds and returns a Car object based on the list of data provided
def parse_car_from_data_lines(car_data_lines):
    carList = car_data_lines.split(",")
    name = carList[0]
    carType = carList[1]
    carRange = carList[2]
    cost = carList[3]
    seats = carList[4]
    saving = carList[5]
    batterySize = carList[6]
    emissions = 0
    link = carList[7]
    costAnalysis = []
    car = Car(name, carType, carRange, cost, seats, saving, batterySize, link, costAnalysis, emissions)
    return car

# calculates cost analysis for gas and electrical cars
def cost_analysis(kilo_per_year, location):
    electricalCharge = float(prov[location]/100)
    for x in range(0, 5):
        for i in list_of_cars:
            if i.carType == 'ZEV':
                charges = kilo_per_year / int(i.carRange)
                chargeCost = electricalCharge * float(i.batterySize)
                cost = charges * chargeCost
            else:
                litres = (kilo_per_year / 100) * float(i.carRange)
                cost = gasCharge * litres
            i.costAnalysis.append(cost)

# calculates emissions
def emission_analysis():
    for i in list_of_cars:
        if i.carType != 'ZEV':
            i.emissions = (2.33 * float(i.carRange) / 100) + (0.43 * float(i.carRange) / 100) # kg of co2 per km
        
def failCar(x):
    if len(x) > 1:
        minCar = x[0]
        min = 999999
        for i in x:
            if sum(i.costAnalysis) < int(min):
                min = sum(i.costAnalysis)
                minCar = i
    
        for i in x:
            if sum(i.costAnalysis) != min:
                x.remove(i)


@app.route('/', methods = ['GET', 'POST']) 
def home():
  data_file = open("vehicles.txt", "r")
  return parse_car_data()

@app.route('/output', methods = ['GET', 'POST'])
def output():
    request_dict = json.loads(request.data)

    location = request_dict['province']
    minCost = int(request_dict['priceRange'][0])
    maxCost = int(request_dict['priceRange'][1])
    kilo_per_year = int(request_dict['kmPerYear'])
    numSeats = int(request_dict['prefNumberOfSeats'])
    climate = request_dict['climate']

  # 1. receive input from user (will fake for now)    
    minCost = 10000 # consider range
    maxCost = 35000 # consider range
    location = 'NB' # province
    kilo_per_year = 40000 #(high, med, low) -> high 
    numSeats = 5 # consider range

    trueList = list_of_cars

    # reducing cost based on savings
    for i in trueList:
        i.cost = int(i.cost) - int(i.saving)

    # cost analysis
    cost_analysis(kilo_per_year, location)
    emission_analysis()
    #return car_schema.jsonify(list_of_cars)

    # split lists into electrical and gas
    gasList = []
    elecList = []

    for i in trueList:
        if i.carType == 'ZEV':
            elecList.append(i)
        else:
            gasList.append(i)

    # gas List
    count = 0
    for i in gasList:
        if int(i.cost) <= maxCost and int(i.cost) >= minCost:
            count = count + 1

    # check if any in budget
    if (count != 0):
        for i in gasList:
            if int(i.cost) > maxCost or int(i.cost) < minCost:
                gasList.remove(i)
        
        count = 0
        for i in gasList:
            if int(i.seats) == numSeats:
                count = count + 1



        # check if seat num is good
        if (count != 0):
            for i in gasList:
                if int(i.seats) != numSeats:
                    gasList.remove(i)
            
            failCar(gasList)
        else:
            failCar(gasList)
    else:
        failCar(gasList)
                
    minCost = 10000 
    maxCost = 35000 

    # elec List
    count = 0
    for i in elecList:
        if int(i.cost) <= maxCost and int(i.cost) >= minCost:
            count = count + 1

    # check if any in budget
    if count != 0:
        for i in elecList:
            if int(i.cost) > maxCost or int(i.cost) < minCost:
                elecList.remove(i)

        return car_schema.jsonify(elecList)     
        
        count = 0
        for i in elecList:
            if int(i.seats) == numSeats:
                count = count + 1
        
        # check if seat num is good
        if (count != 0):
            for i in elecList:
                if int(i.seats) != numSeats:
                    elecList.remove(i)

            return car_schema.jsonify(elecList)

            failCar(elecList)
        else:
            failCar(elecList)
    else:
        failCar(elecList)

    retList = [elecList[0], gasList[0]]
    return car_schema.jsonify(retList)

    #return 5


# driver function 
if __name__ == '__main__': 
	app.run(debug = True) 


#Notes:

#receive JSON object -> send back JSON object

    #POST message to be recieved#
    # in teams

    # return one gas and one electric