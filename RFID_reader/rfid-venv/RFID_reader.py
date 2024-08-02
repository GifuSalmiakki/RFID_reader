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



def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    rfidReader = RFIDReader()
    readers = [("reader1", 5),
               ("reader2", 6)]

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