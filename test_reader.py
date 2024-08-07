from time import sleep
import RPI.GPIO as GPIO
from mfrc522 import MFRC522

reader = MFRC522()

status =  None
while status != reader.MI_OK:
	(status, TagType) = reader.Request(reader.PICC_REQIDL)
	if status == reader.MI_OK:
		print("Connection Success!")
GPIO.cleanup()
