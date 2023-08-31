import serial
import time
import string
import pynmea2
import requests

#the url  where to send the data 
url='http://192.168.1.188:8080/Bus/updateBusPosition/1'

while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	newdata=newdata.decode('latin-1')

	if newdata[0:6] == "$GPRMC":
		time.sleep(1)
		newmsg=pynmea2.parse(newdata)
		lat=newmsg.latitude
		lng=newmsg.longitude
		


		gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
		print(gps)
		#data to be sent
		data={
       			 'latitude':lat,
       			 'longitude':lng
			}
		try:
       			#sending the http Post request
			response=requests.post(url,json=data)
			#check if the request was successful
			if response.status_code==200:
				print("Data sent successfully!")
			else:
				print(f"Failed to send Data .Status Code:{response.status_code}")
		except requests.exceptions.RequestException as e :
        		print(f"An error occurred:{e}")
