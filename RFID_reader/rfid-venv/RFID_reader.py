import RPi.GPIO as GPIO #(might not be the best library)
from mfrc522 import MFRC522
import spidev
import signal

# storing if cards have been read,
# since that's the only thing we're concerned with
cardsRead = {}
CARD_AMOUNT = 2
for card in range(CARD_AMOUNT):
    cardsRead[card] = False

class RFIDReader():

    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = MFRC522()
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = spd

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

        for loop_id in self.boards:
            GPIO.output(self.boards[loop_id], loop_id == readerID)
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
    readers = [("reader1", 5),
               ("reader2", 6)]
    for r in readers:
        RFIDReader.addBoard(r[0], r[1])

    cardsInPlace = False
    # reading each reader one at a time
    while not cardsInPlace:
        for r in readers:
            try:
                cardID, cardData = rfidReader.read(r[0])
                # card was read, set corresponding value to True
                if cardID != None:
                    cardsRead[r] = True
            except Exception as exception:
                print("Execption: "+ exception)

        # all cards read on one pass, all cards in place
        if cardsRead[0] == cardsRead[1] == True:
            print("All cards in place :)")
            cardsInPlace = True

    GPIO.cleanup()