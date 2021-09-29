import RPi.GPIO as GPIO
import time

dac = [26,19,13,6,5,11,9,10]
bits = len(dac)
troykaModule = 17
comparator = 4
levels = 2**bits
maxVoltage = 3.3

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac, signal)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(troykaModule,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def adc():
    for value in range(256):
        bin2dac(value)
        voltage = value / levels * maxVoltage
        time.sleep(0.001)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 0:
            print("Digital value = {:^3}, Analog voltage = {:.2f} V".format(value,voltage))
            break

try:
    while True:
        adc()

except ArithmeticError:
    print("not")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(troykaModule, GPIO.LOW)
    GPIO.cleanup(troykaModule)
    GPIO.cleanup(comparator)
    print("GPIO cleanup completed")