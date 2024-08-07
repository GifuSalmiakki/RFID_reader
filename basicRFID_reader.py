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

for card in range(CARD_AMOUNT-1):
    cardsRead[card] = False

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
    cardsInPlace = False

    # reading each reader one at a time
    while not cardsInPlace:
        for r in readers:
            try:
                cardID = rfidReader.readCard(r[0])
                print("Card "+str(cardID)+" read")
                # card was read, set corresponding value to True
                cardsRead[r] = True
            except KeyboardInterrupt:
                GPIO.cleanup()

            # all cards read on one pass, all cards in place
        values = groupby(cardsRead.values())
        if all(value == True for value in values):
            print("All cards in place :)")
            cardsInPlace = True

    GPIO.cleanup()

if __name__ == "__main__":
    main()
