import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import signal
from typing import Self
from itertools import groupby

# storing if cards have been read,
# since that's the only thing we're concerned with
cardsRead = {}
CARD_AMOUNT = 1
GPIO_READER1 = 25
readers = [("reader1", GPIO_READER1)]

class RFIDReader():

    def __init__(self) -> Self:
        self.reader = SimpleMFRC522()

    def readCard(self) -> Self:
        cardID, data = self.reader.read()
        return cardID

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    rfidReader = RFIDReader()
    cardInPlace = False

    # reading each reader one at a time
    while not cardInPlace:

        try:
            cardID = rfidReader.readCard()
            print("Card "+str(cardID)+" read")
            # card was read, set corresponding value to True
            cardInPlace = True
        except Exception as exception:
            print("Execption: " + str(exception))

        if cardInPlace:
            print("Card in place :)")

    GPIO.cleanup()

if __name__ == "__main__":
    main()
