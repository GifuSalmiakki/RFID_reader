import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
from typing import Self
from itertools import groupby

# storing if cards have been read,
# since that's the only thing we're concerned with
cardsRead = {}
CARD_AMOUNT = 1
GPIO_READER1 = 25
readers = [("reader1", GPIO_READER1)]

for card in range(CARD_AMOUNT):
    cardsRead[card] = False

class RFIDReader():
    def __init__(self, bus=0, device=0, spd=1000000) -> Self:
        self.reader = SimpleMFRC522()
        self.close()
        self.bus
        self.boards = {}

        self.bus = bus
        self.device = device
        self.spd = spd
    def reinit(self) -> Self:
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self) -> Self:
        self.reader.READER.spi.close()

    def readCard(self, readerID) -> Self:
        cardID, data = self.reader.read()
        return cardID

    def addBoard(self, readerID, pin) -> Self:
        self.boards[readerID] = pin
        GPIO.setup(pin, GPIO.OUT)
        print(pin)

    def selectBoard(self, readerID) -> Self:
        if not readerID in self.boards:
            print("Reader ID" + readerID + " not found")
            return False

        for id in self.boards:
            GPIO.output(self.boards[id], id == readerID)
        return True

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
            except Exception as exception:
                print("Execption: "+ str(exception))

            # all cards read on one pass, all cards in place
        values = groupby(cardsRead.values())
        if all(value == True for value in values):
            print("All cards in place :)")
            cardsInPlace = True

    GPIO.cleanup()

if __name__ == "__main__":
    main()

