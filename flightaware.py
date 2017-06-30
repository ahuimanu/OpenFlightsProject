import requests, json, pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

"""
REST / JSON

FlightXML 2.0 can also be accessed using a light-weight "Representational state transfer" (REST) inspired protocol that
returns its responses encoded in "JavaScript Object Notation" (JSON) format.
This allows FlightXML to be used in environments in which it is inconvenient or impossible to invoke SOAP services,
such as mobile phone applications, web browser applications, or server-side JavaScript environments.

To access any method, simply perform either a GET or POST request
to http://flightxml.flightaware.com/json/FlightXML2/METHODNAME using standard CGI-style representation of the arguments.
All requests made must supply the username and API Key as a "basic" Authorization HTTP header.

For example, the following URL is how you might request the current weather at
John F. Kennedy airport (KJFK) in New York:
http://flightxml.flightaware.com/json/FlightXML2/MetarEx?airport=KJFK&startTime=0&howMany=1&offset=0

Requests can be returned in "JSONP" format, allowing a web page to load the response in a way that avoids the same-domain
security restrictions enforced by some browsers. To do this, simply specify the
optional argument "jsonp_callback" with a value that is the name of the
JavaScript function that should be invoked with the JSON data.
"""

#replace with your username and key
user = "xxxxxxxx"
key = "xxxxxxxx"

#FlightAwareArrive class
class FlightAwareArrive:

    def __init__(self, actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                 destinationCity, destinationName, ident, origin, originCity, originName):
        self.actualarrivaltime = datetime.fromtimestamp(actualarrivaltime)
        self.actualdeparturetime = datetime.fromtimestamp(actualdeparturetime)
        self.aircrafttype = aircrafttype
        self.destination = destination
        self.destinationCity = destinationCity
        self.destinationName = destinationName
        self.ident = ident
        self.origin = origin
        self.originCity = originCity
        self.originName = originName

    def displayFlightAwareArrivalForPrint(self):
        output = "Flight {0} ({1})\n" + \
                 "Departing: {2}-{3}({4}) at {5}\n" + \
                 "Arriving:  {6}-{7}({8}) at {9}\n"
                 
        return output.format(self.ident, self.aircrafttype, self.originName, self.originCity, self.origin,
                             self.actualdeparturetime, self.destinationName, self.destinationCity,
                             self.destination, self.actualarrivaltime)
    

    def displayFlightAwareArrivalForCSV(self):
        return ""
    

    def writeFlightAwareArrivalToDB(self):

        #change the databse information to reflect your own
        #open database connection
        db = pymysql.connect('servername','username','password','tablename')

        #prepare a cursor object
        cursor = db.cursor()

        #NOTE: Take not of your own table name and use that table name
        #prepare SQL statement
        statement = "INSERT INTO FlightArrival(ACTUAL_ARRIVAL_TIME, " + \
                    "ACTUAL_DEPARTURE_TIME, AIRCRAFT_TYPE, DESTINATION, " + \
                    "DESINTATION_CITY, DESTINATION_NAME, IDENT, ORIGIN, " + \
                    "ORIGIN_CITY, ORIGIN_NAME) VALUES (%s, %s, %s," + \
                    "%s, %s, %s, %s, %s, %s, %s)"

        data = (self.actualarrivaltime, self.actualdeparturetime, self.aircrafttype,
                self.destination, self.destinationCity, self.destinationName,
                self.ident, self.origin, self.originCity, self.originName)

        #print(statement)

        #give it a shot
        try:
            #Execute the SQL command
            cursor.execute(statement, data)
            #commit/save changes
            db.commit()
        except Exception as exp:
            #rollback changes in case of error
            print('things went bad: ' + str(exp))
            db.rollback()

        #disconnect from server
        db.close()
        
        return

    
def getFlightAwareArrivals(airport, filterType, howMany, offset, user, key):

    #hold arrivals objects
    arrivals = []    

    #Service URL
    url = "http://flightxml.flightaware.com/json/FlightXML2/Arrived?airport=" + airport + \
          "&filter=" + filterType + "&howMany=" + str(howMany) + "&offset=" + str(offset)

    #make request
    req = requests.get(url, auth=(user, key))
    
    #translate to JSON
    flightaware = req.json()

    for arrival in flightaware["ArrivedResult"]["arrivals"]:
        #int actual time of arrival (seconds since 1970)
        actualarrivaltime   = arrival["actualarrivaltime"]
        #int actual time of departure (seconds since 1970)
        actualdeparturetime = arrival["actualdeparturetime"]	
        #aircrafttype string	aircraft type ID
        aircrafttype        = arrival["aircrafttype"]
        #destination string the destination ICAO airport ID
        destination         = arrival["destination"]
        #destinationCity string
        destinationCity     = arrival["destinationCity"]
        #destinationName string
        destinationName     = arrival["destinationName"]
        #ident string flight ident or tail number
        ident               = arrival["ident"]
        #origin string the origin ICAO airport ID
        origin              = arrival["origin"]
        #originCity string
        originCity          = arrival["originCity"]
        #originName string
        originName          = arrival["originName"]

        arrivals.append(FlightAwareArrive(actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                                          destinationCity, destinationName, ident, origin, originCity, originName))

    return arrivals


def getFlightAwareMetarEx(airport, user, key):

    #service URL
    url = "http://flightxml.flightaware.com/json/FlightXML2/MetarEx?airport=" + airport + \
          "&startTime=0&howMany=1&offset=0"

    #make request
    req = requests.get(url, auth=(user, key))

    #translate to JSON
    fajson = req.json()

    #parse elements
    airport         = fajson["MetarExResult"]["metar"][0]["airport"]
    temperature     = fajson["MetarExResult"]["metar"][0]["temp_air"]
    dewpoint        = fajson["MetarExResult"]["metar"][0]["temp_dewpoint"]
    pressure        = fajson["MetarExResult"]["metar"][0]["pressure"]
    wind_direction  = fajson["MetarExResult"]["metar"][0]["wind_direction"]
    wind_speed      = fajson["MetarExResult"]["metar"][0]["wind_speed"]

    return "Airport: {0} Temp: {1} Dewpoint: {2} Pressure: {3} {4} degrees at {5} knots".format(airport,
                                                                                                temperature,
                                                                                                dewpoint,pressure,
                                                                                                wind_direction, wind_speed)    


def printFlightAwareArrivals(arrivals):

    for arrival in arrivals:
        print(arrival.displayFlightAwareArrivalForPrint())

    return


def writeFlightAwareArrivalsToDB(arrivals):

    for arrival in arrivals:
        arrival.writeFlightAwareArrivalToDB()

    return


############### MAIN PROGRAM ###############
#call Metar
result = getFlightAwareMetarEx("EGLL", user, key)
print(result)

#call Arrivals
arrivals = getFlightAwareArrivals("EGLL", "airline", 10, 0, user, key)
printFlightAwareArrivals(arrivals)
writeFlightAwareArrivalsToDB(arrivals)


