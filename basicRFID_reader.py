import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from typing import Self

class RFIDReader():

    def __init__(self) -> Self:
        self.reader = SimpleMFRC522()

    def readCard(self) -> Self:
        cardID, data = self.reader.read()
        return cardID

def main():

    rfidReader = RFIDReader()
    cardInPlace = False
    
    while not cardInPlace:
        try:
            cardID = rfidReader.readCard()
            print("Card "+str(cardID)+" read")
            # card was read, set corresponding value to True
            cardInPlace = True
        except KeyboardInterrupt:
            GPIO.cleanup()

    if cardInPlace:
        print("Card in place :)")

    GPIO.cleanup()

if __name__ == "__main__":
    main()
