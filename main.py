import requests
from datetime import datetime
import os
import json
from geojson import Feature, Point, FeatureCollection, dump

#Function to Build the Filepath to Save the GEOJSON Files

def FileName():
    filepath = os.getcwd()
    currentDateAndTime = datetime.now()
    name = "AreaTemp-"+str(currentDateAndTime.year)+str(currentDateAndTime.month) + str(currentDateAndTime.day)+".json"
    geojsonFile = os.path.join(filepath,name)
    return geojsonFile

#Function to get the grid number from the latitude and longitude
def pullURLfromCoords(x,y):
    APIURL = "https://api.weather.gov/points/" + str(x)+"," +str(y)
    response =  requests.get(APIURL) 
    GridURL = response.json()["properties"]["forecast"]
    return GridURL

#Function to pull the forecast from the grid and return as a feature a town
def pullForecast(PlaceName, URL):
    response =  requests.get(URL) 
    WeeklyData = response.json()
    WeeklyData["properties"]["updated"]
    Details = WeeklyData["properties"]["periods"]
    #This dictionary holds temperatures for every day of the week
    ExportInfo = {}
    for x in Details:
        date = x['name']    
        ExportInfo[date] = x['temperature']
    Town = Point((29.086575, -95.279697))
    TownFeature = Feature(geometry=Town, properties={"Name":PlaceName,"Temperature": ExportInfo["Tonight"]})
    return TownFeature

#This Dictionary specifies which cities to run through the weather API for forecasts
CoordDict = {
    "Houston" : [29.752518, -95.359294],
    "Demi John" : [29.086575, -95.279697]
}

FeatureDict = {}
towns=[]

for place in CoordDict:
    ForecastURL = pullURLfromCoords(CoordDict[place][0], CoordDict[place][1])
    featuredata = pullForecast(place, ForecastURL)
    FeatureDict[place] = featuredata
    towns.append(featuredata)

geoFile = FileName()
regionaldata = FeatureCollection(towns)

with open(geoFile, 'w') as f:
    dump(regionaldata,f)


#THIS LINE IS SPECIFICALLY FOR USE WITHIN QGIS
#Import the GEOSON to QGIS
vlayer = QgsVectorLayer(r"C:\Users\Chabl\Desktop\AreaTemperatures.geojson","mygeojson","ogr")
QgsProject.instance().addMapLayer(vlayer)
