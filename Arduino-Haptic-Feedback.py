import numpy as np
from PIL import ImageGrab, Image
import cv2
import pytesseract
import math
import serial

class Process:
    def __init__(self):
        self.currentHealth = 100
        self.ocrErr = False

    def processImg(self, greyImg):
        self.currentHealth
        txt = pytesseract.image_to_string(greyImg)
        print(txt)
        if txt == '' or txt == '|1oo':
            return True
        try:        
            health = int(txt)
            self.ocrErr = False
        except:
            health = self.currentHealth
            if not self.ocrErr:
                health = self.currentHealth - 1
                self.ocrErr = True

        if health < self.currentHealth:
            self.currentHealth = health
            return True
        return False

    ard = serial.Serial()
    ard.baudrate = 9600
    ard.timeout = 1
    ard.setDTR(False)
    ard.setRTS(False)
    ard.open()
    return ard

def main():
    ard = getPort()
    process = Process()
    while(True):
        x = 200
        y = 800

        offx = 60
        offy = 25
        img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy)).convert('L')
        
        img = np.array(img)
        cv2.imshow('window', img)
        
        ard.write('1'.encode() if process.processImg(img) else '0'.encode())

        if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break
    ard.close()

if __name__ == '__main__':
	main()

print("Let the games begin.")