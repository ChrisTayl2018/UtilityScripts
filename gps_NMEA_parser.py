import serial
import os 
import datetime
from time import time 


# Receiver details  
port = "/dev/ttyUSB0"
baud = 38400


def parseGPS(data):

# NMEA GGA String 
# Message ID, UTC of Possition Fix, Latitude, Direction of lattitude, Longitude, Direction of Longitude, GPS Quality Indicator, Number of SV's, HDOP, Orthometric height, Meters, Geoid Seperation, Meters, Age of differential GPS data
 

    if(data[0:6] == "$GNGGA"):
        sdata = data.split(",")
        if sdata[2] == 'V':
            print "no GGA Strings available \n"
            return
        print "-------------------\n",
        print "---PARSING GNGGA---\n",
        print "-------------------\n",

        sentenceId = "$GNGGA"
   
        # GPS Time in NMEA sentence  
        gps_time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]

        # System  Time
        OS_time = datetime.datetime.now()       

       # epoch_time = int((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())
        epoch_time = int(datetime.datetime.now().strftime("%s")) * 1000
        
        lat = decode(sdata[2]) #latitude

        directionLatitude = sdata[3]     #latitude direction N/S

        lon = decode(sdata[4]) #longitute

        directionLongitude = sdata[5]     #longitude direction E/W

        gpsQualityIndicator = sdata[6]       #Speed in knots

        numOfSVs = sdata[7]    #True course

        hdop = sdata[8]    # Quality of GPS < 1 = good GPS signal

        orthHeight = sdata[8]
              
        # Populate output list
        list = [OS_time, epoch_time, sentenceId, gps_time, lat, directionLatitude, lon, directionLongitude, gpsQualityIndicator, numOfSVs, hdop]
        
        # Debug outputs to dump to command window
        #print "Arrival time : %s , Epochtime : %s , GPS time : %s, latitude : %s(%s), longitude : %s(%s)"  %  (OS_time, epoch_time, gps_time, lat, directionLatitude, lon, directionLongitude)
        #print "GPS Qual : %s, numberSats: (%s), HDOP: %s" %  (gpsQualityIndicator, numOfSVs, hdop)
	
        return list
 
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"





 
print "Receiving GPS data"

# Open the serial port 
ser = serial.Serial(port, baudrate = baud, timeout = 0.5)


# Open a logger text file for NMEA data 
outputFile = open('nmeaLogger.csv', 'w')

# Start the measurement counter 
measurement_count = 0
gga_count = 0

while True:
   
   # Read serial data  
   data = ser.readline()
   
   # Create NMEA list 
   nmeaList = parseGPS(data)
     
   # Check if return value is a list of values
   boolean_val = isinstance(nmeaList, list)

   if boolean_val == True:
      
      # NMEA String counter 
      outputFile.write(str(measurement_count) + ', ')
      # NMEA GGA Counter 
      outputFile.write(str(gga_count) + ', ')

      # Debug output 
      # print nmeaList
  
      for x in range(len(nmeaList)):

          # Convert nmea list element to a string value 
          nmeaElement = str(nmeaList[x])

          # Write the nmea output to file
          outputFile.write(nmeaElement + ',  ')
      
     # Create a new line 
      outputFile.write("\n")

      gga_count = gga_count + 1

   measurement_count = measurement_count +  1

outputFile.close()


