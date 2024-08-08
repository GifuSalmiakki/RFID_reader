import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from typing import Self
import time

CARD_AMOUNT = 1
GPIO_READER1 = 25
readers = [("reader1", GPIO_READER1)]

class RFIDReader():

    def __init__(self) -> Self:
        self.reader = SimpleMFRC522()

    def readCard(self, readerID) -> Self:
        cardID, data = self.reader.read()
        return cardID

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    rfidReader = RFIDReader()
    cardInPlace = False

    # reading each reader one at a time
    while not cardInPlace:
        for r in readers:
            try:
                cardID = rfidReader.readCard(r[0])
                print("Card "+str(cardID)+" read")
                # card was read, set corresponding value to True
                cardInPlace = True
            except KeyboardInterrupt:
                GPIO.cleanup()

        if cardInPlace:
            print("Card in place :)")
            cardsInPlace = True

        time.sleep(1)
        
    GPIO.cleanup()

if __name__ == "__main__":
    main()
