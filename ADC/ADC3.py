import RPi.GPIO as GPIO
import time

dac = [26,19,13,6,5,11,9,10]
leds = [21,20,16,12,7,8,25,24]
bits = len(dac)
troykaModule = 17
comparator = 4
levels = 2**bits
maxVoltage = 3.3

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2set(value, pins):
    signal = decimal2binary(value)
    GPIO.output(pins, signal)
#    return signal

def ledPanel(signal):
    led = 255
    while led > (signal / 255 * 8):
        led = led >> 1
    bin2set(led, leds)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(leds,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(troykaModule,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)
def adc():
    signal = 128
    for value in range(7,0,-1):
        bin2set(signal, dac) 
        voltage = signal / levels * maxVoltage
        time.sleep(0.001)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 0:
            signal -= 2**value
        signal += 2**(value-1)
    bin2set(signal, dac)
    print("Digital value = {:^3}, Analog voltage = {:.2f} V".format(signal,voltage))
    ledPanel(signal)


try:
    while True:
        adc()

except ArithmeticError:
    print("not")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    GPIO.output(troykaModule, GPIO.LOW)
    GPIO.cleanup(troykaModule)
    GPIO.cleanup(comparator)
    print("GPIO cleanup completed")