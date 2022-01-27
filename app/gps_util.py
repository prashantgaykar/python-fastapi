
from io import TextIOWrapper
import threading
from time import sleep
import os

dir_path = os.path.dirname(__file__)
loc_f = 'loc.kml'
file_name = os.path.join(dir_path, loc_f)
data_file: TextIOWrapper = None
timer: threading.Timer = None

valid_data = "GPS123,1,2022-1-26T23:37:14,19020999,73096803,N,7,30,270,0,5500"
invalid_data = "GPS123,0,2022-1-26T23:33:57,0,0,N,0,231,0,0,0"
file_start = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Testing My KML</name>
	<Style id="line_color">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Start to End</name>
	  <styleUrl>#line_color</styleUrl>
      <LineString>
		<extrude>1</extrude>
        <tessellate>1</tessellate>
        <coordinates>
"""

file_end = """    </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""


def get_file_path():
    return file_name


def get_file_name():
    return loc_f


def create_location_file():
    global data_file
    data_file = open(file_name, 'w')
    data_file.write(file_start)


def save_location_data(rawData: str):
    global data_file
    global timer
    if(timer is not None):
        timer.cancel()
    timer = threading.Timer(30, close_location_file)
    timer.start()
    if(rawData.startswith("GPS123")):
        chunks = rawData.split(",")
        if(chunks[1] == "1"):
            if(data_file is None):
                create_location_file()
            elif(data_file.closed):
                del(data_file)
                create_location_file()

            latitude = int(chunks[3]) / (10 ** 6)
            longitude = int(chunks[4]) / (10 ** 6)
            points = str(longitude) + "," + str(latitude) + ",0\n"
            data_file.write(points)
            print("added data...")
        else:
            print("INVALID DATA")


def close_location_file():
    global data_file
    print("\nclosing file...")
    data_file.write(file_end)
    data_file.close()
