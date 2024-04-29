import requests
import json
from geojson import Feature, Point, FeatureCollection, dump

def pullURLfromCoords(x,y):
    APIURL = "https://api.weather.gov/points/" + str(x)+"," +str(y)
    response =  requests.get(APIURL) 
    GridURL = response.json()["properties"]["forecast"]
    return GridURL


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


CoordDict = {
    "Houston" : [29.752518, -95.359294],
    "Demi John" : [29.086575, -95.279697]
}

FeatureDict = {}
towns=[]

for place in CoordDict:
    ForecastURL = pullURLfromCoords(CoordDict[place][0], CoordDict[place][1])
    print(ForecastURL)
    featuredata = pullForecast(place, ForecastURL)
    print(featuredata)
    FeatureDict[place] = featuredata
    towns.append(featuredata)
    
print(FeatureDict)


regionaldata = FeatureCollection(towns)
with open(r'C:\Users\Desktop\AreaTemperatures.geojson', 'w') as f:
    dump(regionaldata,f)
