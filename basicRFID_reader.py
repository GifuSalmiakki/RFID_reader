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
boards = {}

for card in range(CARD_AMOUNT):
    cardsRead[card] = False


class RFIDReader():

    def __init__(self):
        self.reader = SimpleMFRC522

    def readCard(self, readerID):
        if not self.selectBoard(readerID):
            return None
        cardID, data = self.reader.read()
        return cardID

    def addBoard(self, readerID, pin):
        boards[readerID] = pin
        GPIO.setup(pin, GPIO.OUT)
        print("Reader connected to pin: " +str(pin))
        return

    def selectBoard(self, readerID):
        if not readerID in boards:
            print("Reader ID" + readerID + " not found")
            return False
        for id in boards:
            GPIO.output(boards[id], id == readerID)
        return True

def main():
    # refer to pins by "GPIO"-numbers on the board
    GPIO.setmode(GPIO.BCM)
    rfidReader = RFIDReader()
    cardsInPlace = False

    for r in readers:
        RFIDReader.addBoard(RFIDReader, r[0], r[1])

    # reading each reader one at a time
    while not cardsInPlace:
        for r in readers:
            try:
                cardID = rfidReader.reader.readCard(r[0])
                print("Card "+cardID+" read")
                # card was read, set corresponding value to True
                if cardID != None:
                    cardsRead[r] = True
            except Exception as exception:
                print("Execption: "+ str(exception))

        # all cards read on one pass, all cards in place
        if cardsRead[0] == True:
            print("All cards in place :)")
            cardsInPlace = True

    GPIO.cleanup()

if __name__ == "__main__":
    main()
