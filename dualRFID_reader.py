import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
from typing import Self
from itertools import groupby
import time

# storing if cards have been read,
# since that's the only thing we're concerned with
cardsRead = {}
CARD_AMOUNT = 1
GPIO_READER1 = 7 # CE1
GPIO_READER2 = 8 # CE0
readers = [("reader1", GPIO_READER1), ("reader2", GPIO_READER2)]


for card in range(CARD_AMOUNT):
    cardsRead[card] = False

class RFIDReader():
    def __init__(self) -> Self:
        self.reader = SimpleMFRC522()
        self.boards = {}
        #self.reader.READER.spi.no_cs = True
    #def reinit(self):
        #self.reader.READER.spi = spidev.SpiDev()
        #self.reader.READER.spi.open(0, 0)
        #self.reader.READER.spi.max_speed_hz = 1000000
        #self.reader.MFRC522_Init()

    #def close(self):
        #self.reader.READER.spi.close()

    def readCard(self, readerID) -> Self:
        if not self.selectBoard(readerID):
            return None
        else:
            GPIO.setup(self.boards[readerID], GPIO.IN)
        cardID, data = self.reader.read()
        return cardID

    def addBoard(self, readerID, pin) -> Self:
        self.boards[readerID] = pin
        GPIO.setup(pin, GPIO.OUT)
        print(str(readerID))

    def selectBoard(self, readerID) -> Self:
        if not readerID in self.boards:
            print("Reader ID" + str(readerID) + " not found")
            return False
        for id in self.boards:
            GPIO.input(self.boards[id], id == readerID)
        return True

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    cardsInPlace = False

    rfidReader = RFIDReader()
    for r in readers:
        rfidReader.addBoard(r[0], r[1])

    # reading each reader one at a time
    while not cardsInPlace:
        for r in readers:
            try:
                GPIO.setup(r[1], GPIO.IN)
                cardID = rfidReader.readCard(r[0])
                if cardID != None:
                    print("Card "+str(cardID)+" read")
                    # card was read, set corresponding value to True
                    cardsRead[r] = True
            except Exception as exception:
                print("Execption: "+ str(exception))

            # all cards read on one pass, all cards in place
        values = groupby(cardsRead.values())
        if all(value == True for value in values):
            print("All cards in place :)")
            cardsInPlace = True

        time.sleep(1)

    GPIO.cleanup()

if __name__ == "__main__":
    main()

