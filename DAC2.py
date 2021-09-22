import RPi.GPIO as GPIO
import time

dac = [26,19,13,6,5,11,9,10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)
    return signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial = GPIO.LOW)

try:
    while True:
        inputStr = input("Enter period ('q' to exit) > ")
        if inputStr.isdigit():
            period = int(inputStr)
            value = 0
            n = -1
            while True:
                if value % 255 == 0 or value < 1:
                    n*=-1
                signal = bin2dac(value)
                value = value + n
                time.sleep(0.1 * period)

        elif inputStr == 'q':
            break
        else:
            print("try again")

except ArithmeticError:
    print("not")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")