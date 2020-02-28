from flask import Flask, request
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import googlemaps
import os
import requests, json
from shapely.geometry import Point, Polygon
import datetime


app = Flask(__name__)


@app.route("/sms", methods = ['GET', 'POST'])
# request = requests.get('https://maps.googleapis.com/maps/api/js?key=AIzaSyAAwuExTdfzuBbRtB1RufGzcUBzmV4YYIY&callback=initMap')



def main():
    #body = input("Where to where? ")
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    currentDT = datetime.datetime.now()
   

    if body.find(":", 0, len(body)) == -1 :
        starting = "" +body[0: body.find(" to ", 0, len(body))]
        end = "" + body[body.find(" to ", 0, len(body))+4:len(body)]
    else :
        currentDT = datetime.time(int(body[body.find(":", 0, len(body))-2:body.find(":", 0, len(body))]), int(body[body.find(":", 0, len(body))+1:len(body)]), 0)
        starting = "" + body[0: body.find(" to ", 0, len(body))]
        end = "" + body[body.find(" to ", 0, len(body))+4:body.find(":", 0, len(body))-2]

        print(starting)
        print(end)
        print(currentDT)
    starting, startLat, startLng = location_finder(starting)
    end, endLat, endLng = location_finder(end)
    directions = starting + " to " + end
    print(directions)
    LXstops = {'Livi Plaza' : {'lat' : "40.525088", 'lng' : "-74.438634"},
            'Livi Student Center' : {'lat' : "40.524063", 'lng' : "-74.436528"},
            'the Quads' : {'lat' : "40.520077", 'lng' : "-74.433289"},
            'Scott Hall' : {'lat' : "40.499219", 'lng' : "-74.447935"},
            'College Ave Student Center' : {'lat' : "40.503521", 'lng' : "-74.45235"},
            'SAC' : {'lat' : "40.504134", 'lng' : "-74.449271"}}
    Bstops = {'Livi Plaza' : {'lat' : "40.525088", 'lng' : "-74.438634"}
                , 'Livi Student Center' : {'lat' : "40.524063", 'lng' : "-74.436528"}
                , 'Quads' : {'lat' : "40.520077", 'lng' : "-74.433289"}
                , 'Werb Side' : {'lat' : "40.518650", 'lng' : "-74.461499"}
                , 'Hill Center' : {'lat' : "40.521917", 'lng' : "-74.463237"}
                , 'Science Building' : {'lat' : "40.523908", 'lng' : "-74.464264"}
                , 'Library of Science' : {'lat' : "40.526185" , 'lng' : "-74.465880"}
                , 'Busch Suites' : {'lat' : "40.525963" , 'lng' : "-74.459045"}
                , 'Busch Student Center' :  {'lat' : "40.523788" , 'lng' :  "-74.458201"}}
    Hstops = {'Scott Hall' : {'lat' : "40.499219", 'lng' : "-74.447935"},
            'College Ave Student Center' : {'lat' : "40.503521", 'lng' : "-74.45235"},
            'SAC' : {'lat' : "40.504134", 'lng' : "-74.449271"},
            'Werb Main Entrance' : {'lat' : "40.518745", 'lng' : "-74.459769"},
            'Buell Apartments' : {'lat': "40.521724", 'lng' : "-74.456752"},
            'Busch Student Center' :  {'lat' : "40.523788" , 'lng' :  "-74.458201"},
            'Davidson Hall' : {'lat' : "40.525963" , 'lng' : "-74.459045"},
            'Library of Science' : {'lat' : "40.526185" , 'lng' : "-74.465880"},
            'ARC Buildings' : {'lat' : "40.523698" , 'lng' : "-74.464918"},
            'Hill Center' : {'lat' : "40.521917", 'lng' : "-74.463237"},
            }
            
    Astops = {'Scott Hall' : {'lat' : "40.499219", 'lng' : "-74.447935"},
            'College Ave Student Center' : {'lat' : "40.503521", 'lng' : "-74.45235"},
            'SAC' : {'lat' : "40.504134", 'lng' : "-74.449271"},
            'Werb Main Entrance' : {'lat' : "40.518745", 'lng' : "-74.459769"},
            'Buell Apartments' : {'lat': "40.521724", 'lng' : "-74.456752"},
            'Busch Student Center' :  {'lat' : "40.523788" , 'lng' :  "-74.458201"},
            'Busch Suites' : {'lat' : "40.525963" , 'lng' : "-74.459045"},
            'Library of Science' : {'lat' : "40.526185" , 'lng' : "-74.465880"},
            'Science Building' : {'lat' : "40.523698" , 'lng' : "-74.464918"},
            'Hill Center' : {'lat' : "40.521917", 'lng' : "-74.463237"},
            }
    Fstops = {'College Hall' : {'lat' : "40.485638", 'lng' : "-74.437418" },
            'Red Oak Lane': {'lat' : "40.483104", 'lng' : "-74.437426" },
            'Lipman Hall': { 'lat' : "40.481417", 'lng' : "-74.436096"},
            'Food Science':{ 'lat' : "40.478938", 'lng' : "-74.435928"},
            'Biel Road': {'lat' : "40.480023", 'lng' : "-74.432549"},
            'Henderson': {'lat' : "40.481173", 'lng' : "-74.429139"},
            'Katzenbach': { 'lat' : "40.483018", 'lng' : "-74.431567"},
            'Gibbons': {'lat' : "40.485289", 'lng' : "-74.431976" },
            'Scott Hall' : {'lat' : "40.499219", 'lng' : "-74.447935"},
            'College Ave Student Center' : {'lat' : "40.503521", 'lng' : "-74.45235"},
            'SAC' : {'lat' : "40.504134", 'lng' : "-74.449271"}
            }
    REXBstops = {'College Hall' : {'lat' : "40.485638", 'lng' :"-74.437418" },
            'Red Oak Lane': {'lat' : "40.483104", 'lng' : "-74.437426" },
            'Lipman Hall': { 'lat' : "40.481417", 'lng' : "-74.436096"},
            'ARC Buildings' : {'lat' : "40.523698" , 'lng' : "-74.464918"},
            'Hill Center' : {'lat' : "40.521917", 'lng' : "-74.463237"},
            }
    REXLstops = {'College Hall' : {'lat' : "40.485638", 'lng' : "-74.437418" },
            'Red Oak Lane': {'lat' : "40.483104", 'lng' : "-74.437426" },
            'Lipman Hall': { 'lat' : "40.481417", 'lng' : "-74.436096"},
            'Livi Plaza' : {'lat' : "40.525088", 'lng' : "-74.438634"},
            'Livi Plaza' : {'lat' : "40.525088", 'lng' : "-74.438634"}, 
            'Livi Student Center' : {'lat' : "40.524063", 'lng' : "-74.436528"},
            }
            
            


    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    key = ""
    best = ""
    if ((starting == "livi" and end == "college ave") or (starting == "college ave" and end == "livi")) :
        best = "Livi Student Center"
        minDist = 9999999
        for stop in LXstops :
            print (stop)
            r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + LXstops[stop]['lat'] + "," + LXstops[stop]['lng'] + "&key=" + key)
            r = r.json()
            dist = r['rows'][0]['elements'][0]['distance']['value']
            if dist < minDist :
                best = stop
                minDist = dist
    elif (((starting == "buscha" or starting == "buschh") and end == "livi") or (starting == "livi" and (end == "buscha" or end == "buschh"))) :
        best = "Busch Student Center"
        minDist = 9999999
        for stop in Bstops :
            print (stop)
            r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Bstops[stop]['lat'] + "," + Bstops[stop]['lng'] + "&key=" + key)
            r = r.json()
            dist = r['rows'][0]['elements'][0]['distance']['value']
            if dist < minDist :
                best = stop
                minDist = dist
    elif (starting == "college ave" and (end == "buscha" or end == "buschh")):
        best = "College Ave Student Center"
        minDist = 9999999
        if (end == "buscha") :
            for stop in Astops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Astops[stop]['lat'] + "," + Astops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        elif (end == "buschh") :
            for stop in Hstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Hstops[stop]['lat'] + "," + Hstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
    elif ((starting == "buschh" or starting == "buscha") and end == "college ave") :
        best = "Busch Student Center"
        minDist = 9999999
        if (starting == "buscha") :
            for stop in Astops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Astops[stop]['lat'] + "," + Astops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        elif (starting == "buschh") :
            for stop in Hstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Hstops[stop]['lat'] + "," + Hstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
    elif ((starting == "cook" and end == "college ave") or (starting == "college ave" and end =="cook")) :
        best = "College Ave Student Center"
        minDist = 9999999
        for stop in Fstops :
            print (stop)
            r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Fstops[stop]['lat'] + "," + Fstops[stop]['lng'] + "&key=" + key)
            r = r.json()
            dist = r['rows'][0]['elements'][0]['distance']['value']
            if dist < minDist :
                best = stop
                minDist = dist
    elif (starting == "cook" and end == "livi")  :
        best = "Livingston Student Center"
        minDist = 9999999
        if currentDT.hour > 7 and currentDT.hour < 23 :
            for stop in REXLstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + REXLstops[stop]['lat'] + "," + REXLstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        else :
            for stop in Fstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Fstops[stop]['lat'] + "," + Fstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
    elif (starting == "livi" and end == "cook") :
        best = "Livingston Student Center"
        minDist = 9999999
        if currentDT.hour > 7 and currentDT.hour < 23 :
            for stop in REXLstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + REXLstops[stop]['lat'] + "," + REXLstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        else :
            for stop in LXstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + LXstops[stop]['lat'] + "," + LXstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
            
    elif ( starting == "busch" and end == "cook") :
        best = "Busch Student Center"
        minDist = 9999999
        if currentDT.hour > 7 and currentDT.hour < 23 :
            for stop in REXBstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + REXBstops[stop]['lat'] + "," + REXBstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        else :
            for stop in Hstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Hstops[stop]['lat'] + "," + Hstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
            if dist < minDist :
                best = stop
                minDist = dist
    elif (starting == "cook" and end == "busch") :
        best = "Red Oak Lane"
        minDist = 9999999
        if currentDT.hour > 7 and currentDT.hour < 23 :
            for stop in REXBstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + REXBstops[stop]['lat'] + "," + REXBstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
                if dist < minDist :
                    best = stop
                    minDist = dist
        else :
            for stop in Fstops :
                print (stop)
                r = requests.get(url + "origins=" + str(startLat) + "," + str(startLng) + "&destinations=" + Fstops[stop]['lat'] + "," + Fstops[stop]['lng'] + "&key=" + key)
                r = r.json()
                dist = r['rows'][0]['elements'][0]['distance']['value']
            if dist < minDist :
                best = stop
                minDist = dist


    if((currentDT.hour > 2 and currentDT.hour < 6) or (currentDT.hour ==2 and currentDT.minute > 30)):
        best = "None :("

    print ("The closest bus stop is " + best)
    bestStop = "The closest bus stop is " + best + "!"

    if "livi to buschh" in directions.lower() or "buschh to livi" in directions.lower() or "buscha to livi" in directions.lower() or "livi to buscha" in directions.lower():
        if currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <20):
            resp.message("Take B! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "college ave to livi" in directions.lower() or "livi to college ave" in directions.lower():
        if currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <15) :
            resp.message("Take LX! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "buscha to college ave" in directions.lower() or "college ave to buscha" in directions.lower() or "buschh to college ave" in directions.lower() or "college ave to buschh" in directions.lower():
        if currentDT.hour > 7 and currentDT.hour < 21 :
            if "buscha to college ave" in directions.lower() or "college ave to buschh" in directions.lower():
                resp.message("Take A! " + bestStop)
            elif "buschh to college ave" in directions.lower() or "college ave to buscha" in directions.lower():
                resp.message("Take H! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour ==2 and currentDT.minute <30) :
                resp.message("Take H " + bestStop)
        else :
                resp.message("No Bus Route!")
    elif "college ave to cook" in directions.lower() or "cook to college ave" in directions.lower():
        if currentDT.hour > 7 and currentDT.hour < 21 :
            resp.message("Take EE or F! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute < 15) :
            resp.message("Take EE! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "livi to cook" in directions.lower():
        if currentDT.hour > 7 and currentDT.hour < 23 :
            resp.message("Take REXL! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <15):
            resp.message("Take an LX and then an EE! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "cook to livi" in directions.lower() :
        if currentDT.hour > 7 and currentDT.hour < 23 :
            resp.message("Take REXL! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <15):
            resp.message("Take an EE and then an LX! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "buscha to cook" in directions.lower()or "buschh to cook" in directions.lower():
        if currentDT.hour > 7 and currentDT.hour < 23 :
            resp.message("Take REXB! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <15):
            resp.message("Take an H and then an EE! " + bestStop)
        else :
            resp.message("No Bus Route!")
    elif "cook to buscha" in directions.lower() or "cook to buschh" in directions.lower() :
        if currentDT.hour > 7 and currentDT.hour < 23 :
            resp.message("Take REXB! " + bestStop)
        elif currentDT.hour > 6 or currentDT.hour < 2 or (currentDT.hour == 2 and currentDT.minute <15):
            resp.message("Take an EE and then an H! " + bestStop)
        else :
            resp.message("No Bus Route!")
    else:
        resp.message("No Bus Route!")
    return (str(resp))

def location_finder(a_string) :
    # enter your api key here
    api_key = 'AIzaSyAAwuExTdfzuBbRtB1RufGzcUBzmV4YYIY'
    query = a_string

    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"

    # get method of requests module
    # return response object
    r = requests.get(url + 'input=' + query + '&key=' + api_key +'&inputtype=textquery' +'&fields=formatted_address,geometry,name')
               

    # json method of response object convert
    # json format data into python format data
    x = r.json()
    print (x)
    # now x contains list of nested dictionaries
    # we know dictionary contain key value pair
    # store the value of result key in variable y
    y = x['candidates']
    print ('\n')

    z = (y[0]['geometry']['location'])
    pt = Point(z['lat'], z['lng'])
    
    polyca = Polygon([(40.490120, -74.441927), (40.492946, -74.452363), (40.499675, -74.463924), (40.507467, -74.452110), (40.500351, -74.443845)])
    polyli = Polygon([(40.524985, -74.448393), (40.505837, -74.440712), (40.513665, -74.425476), (40.525278, -74.427106), (40.532097, -74.442729)])
    polycd = Polygon([(40.490120, -74.441927), (40.467900, -74.455505), (40.457437, -74.427237), (40.474610, -74.415324), (40.491094, -74.435263)])
    polybu = Polygon([(40.510755, -74.462606), (40.522043, -74.488226), (40.531242, -74.467326), (40.526509, -74.447241), (40.516821, -74.453554)])
    polybuA = Polygon([(40.510755, -74.462606), (40.521020, -74.460552),(40.529854, -74.461346), (40.526509, -74.447241), (40.516821, -74.453554)])
    polybuH = Polygon([(40.510755, -74.462606), (40.522043, -74.488226), (40.531242, -74.467326), (40.529854, -74.461346), (40.521020, -74.460552)])
    if polyca.contains(pt) :
        campus = 'college ave'
    elif polyli.contains(pt) :
        campus = 'livi'
    elif polycd.contains(pt) :
        campus = 'cook'
    elif polybuA.contains(pt) :
        campus = 'buscha'
    elif polybuH.contains(pt) :
        campus = 'buschh'
    else :
        campus = 'livi'
    return campus, z['lat'], z['lng']

if __name__ == "__main__":
   app.run(debug =True)
   #main()
