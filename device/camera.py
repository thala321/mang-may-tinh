from picamera import PiCamera
from time import sleep
import base64
import requests
import serial

def convertImageToBase64():
 with open("/home/pi/Desktop/image.jpg", "rb") as image_file:
     encoded = base64.b64encode(image_file.read())
 return encoded

ser = serial.Serial('/dev/ttyACM0',9600)
s = [0]
camera = PiCamera()
while True:
    read_serial=ser.readline()
    rfidData = read_serial.decode('utf-8');
    if (rfidData):
        # Take image
        camera.capture('/home/pi/Desktop/image.jpg')

        # Covert image to base64
        convertedImage = convertImageToBase64()

        # Send image and rfid to server
        r = requests.post("http://172.16.4.151:3000/data", data={'image': convertedImage,'rfid':rfidData})
        print(r.status_code, r.reason)