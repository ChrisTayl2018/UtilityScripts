import serial
 
port = "/dev/ttyUSB0"
 
## NMEA GNRMC String

def parseGPS(data):
#    print "raw:", data #prints raw data
    if data[0:6] == "$GNRMC":
        sdata = data.split(",")
        if(sdata[2] == 'V'):
            print "No RMC data available\n"
            return
        print "-------------------\n",
        print "---PARSING GNRMC---\n",
        print "-------------------\n",
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
        print "GPS time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s \n" %  (time,lat,dirLat,lon,dirLon,speed,trCourse,date)

## NMEA GGA String 

# Message ID, UTC of Possition Fix, Latitude, Direction of lattitude, Longitude, Direction of Longitude, GPS Quality Indicator, Number of SV's, HDOP, Orthometric height, Meters, Geoid Seperation, Meters, Age of differential GPS data
    time = 0 
    time_old = 0
    if(data[0:6] == "$GNGGA"):
        sdata = data.split(",")
        if sdata[2] == 'V':
            print "no GGA Strings available \n"
            return
        print "-------------------\n",
        print "---PARSING GNGGA---\n",
        print "-------------------\n",

        time_diff = time-time_old
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        time_old = time
        lat = decode(sdata[2]) #latitude
        directionLatitude = sdata[3]     #latitude direction N/S
        lon = decode(sdata[4]) #longitute
        directionLongitude = sdata[5]     #longitude direction E/W
        gpsQualityIndicator = sdata[6]       #Speed in knots
        numOfSVs = sdata[7]    #True course
        hdop = sdata[8]
        orthHeight = sdata[8]
        unitMeasureOrthHeight = 0
        geoidSeperation = 0
        ageOfGPSData = 0
        
        time_df = 0
        msgFreq = 0
        
        print "GPS time : %s, latitude : %s(%s), longitude : %s(%s), time_diff : %s, msg_freq : %s" %  (time,lat, directionLatitude, lon, directionLongitude, time_diff, msgFreq)
        print "GPS Qual : %s, numberSats: (%s), HDOP: %s, Orthemetric Height : %s(%s), Age of data : %s" %  (gpsQualityIndicator, numOfSVs, hdop, orthHeight, unitMeasureOrthHeight, ageOfGPSData)
        print(time_old)
 
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"
 
 
print "Receiving GPS data"
ser = serial.Serial(port, baudrate = 38400, timeout = 0.5)
while True:
   data = ser.readline()
   parseGPS(data)
   
