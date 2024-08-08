import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
from typing import Self
from itertools import groupby
import time
from PIL import Image

CARD_AMOUNT = 2
GPIO_READER1 = 5
GPIO_READER2 = 6
readers = [("reader1", GPIO_READER1), ("reader2", GPIO_READER2)]

class RFIDReader():
    def __init__(self, bus=0, device=0, speed=1000000) -> Self:
        self.reader = SimpleMFRC522()
        self.close()
        self.boards = {}

        self.bus = bus
        self.device = device
        self.speed = speed

    def reinit(self) -> Self:
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.speed
        self.reader.READER.MFRC522_Init()

    def close(self) -> Self:
        self.reader.READER.spi.close()

    def addBoard(self, readerID, pin) -> Self:
        self.boards[readerID] = pin
        GPIO.setup(pin, GPIO.OUT)

    def selectBoard(self, readerID) -> Self:
        if not readerID in self.boards:
            print("readerid " + readerID + " not found")
            return False
        for loop_id in self.boards:
            GPIO.output(self.boards[loop_id], loop_id == readerID)
        return True

    def read(self, readerID) -> Self:

        if not self.selectBoard(readerID):
            return None
        self.reinit()
        cardID, data = self.reader.read_no_block()
        self.close()

        return cardID

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    cardsInPlace = False
    rfidReader = RFIDReader()
    # Chip select pin
    GPIO.setup(8, GPIO.OUT)

    for r in readers:
        rfidReader.addBoard(r[0], r[1])

    # reading each reader one at a time
    while not cardsInPlace:

        bothCardsRead = 0
        for r in readers:
            try:
                cardID = rfidReader.read(r[0])
                if cardID != None:
                    print("Card "+str(cardID)+" read")
                    # card was read, set corresponding value to True
                    bothCardsRead += 1
            except Exception as exception:
                print("Execption: "+ str(exception))

        # all cards read on one pass, all cards in place
        if bothCardsRead == 2:
            cardsInPlace = True
            print("All cards in place! :)")

        time.sleep(1)
    GPIO.cleanup()

if __name__ == "__main__":
    main()

