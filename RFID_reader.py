import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
import signal

# storing if cards have been read,
# since that's the only thing we're concerned with
cardsRead = {}
CARD_AMOUNT = 1
GPIO_READER1 = 25
readers = [("reader1", GPIO_READER1)]

for card in range(CARD_AMOUNT):
    cardsRead[card] = False

class RFIDReader():

    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.close()
        self.bus
        self.boards = {}

        self.bus = bus
        self.device = device
        self.spd = spd


def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, readerID, pin):
        self.boards[readerID] = pin
        GPIO.setup(pin, GPIO.OUT)
        print(pin)

    def selectBoard(self, readerID):
        if not readerID in self.boards:
            print("Reader ID" + readerID + " not found")
            return False

        for id in self.boards:
            GPIO.output(self.boards[id], id == readerID)
        return True

    def read(self, readerID):
        if not self.selectBoard(readerID):
            return None

        self.reinit()
        cardID, cardData = self.reader.read_no_block()
        self.close()
        return cardID

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    rfidReader = RFIDReader()

    for r in readers:
        RFIDReader.addBoard(RFIDReader, r[0], r[1])

    cardsInPlace = False
    # reading each reader one at a time
    while not cardsInPlace:
        for r in readers:
            try:
                cardID = rfidReader.read(r[0])
                # card was read, set corresponding value to True
                if cardID != None:
                    cardsRead[r] = True
            except Exception as exception:
                print("Execption: "+ exception)

        # all cards read on one pass, all cards in place
        if cardsRead[0] == True:
            print("All cards in place :)")
            cardsInPlace = True

    GPIO.cleanup()

if __name__ == "__main__":
    main()
