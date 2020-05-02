#!/usr/bin/python

import time
import picamera
import base64
import requests
# import serial
from serial import *

def convertImageToBase64():
 with open("/data/image.jpg", "rb") as image_file:
     encoded = base64.b64encode(image_file.read())
 return encoded

print("Main")
camera = picamera.PiCamera()
camera.resolution = (320, 240)

while True:
    print('Loop')
    # Init serial connection to Arduino
    ser = Serial('/dev/ttyACM0', 9600)
    s = [0]
    read_serial=ser.readline()
    rfidData = read_serial.decode('utf-8');
    if (rfidData):
        camera.capture('/data/image.jpg')
        convertedImage = convertImageToBase64()
        try:
            headers = {"Origin": "https://www.wes.org",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Connection": "close",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
               "Referer": "https://www.wes.org/appstatus/indexca.aspx", "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "en-US,en;q=0.8,fa;q=0.6", "Content-Type": "application/json"}
            r = requests.post("https://192.168.43.223:5001/api/vehicles", json={"cardId": "foRAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIj", "vehiclePlatesImg": convertedImage, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"}, headers=headers, verify=False)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print (e.response.text)
    time.sleep(2)
