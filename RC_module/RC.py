import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Used pins
dac = [26,19,13,6,5,11,9,10]
leds = [21,20,16,12,7,8,25,24]
troykaModule = 17
comparator = 4

# Constant values
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
period = 0.005

# Binary bit representation of a decimal number
def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

# DAC output
def bin2set(value, pins):
    signal = decimal2binary(value)
    GPIO.output(pins, signal)

# LED output
def ledPanel(signal):
    led = 255
    temp = round(signal / 32)
    while temp < 8:
        led = led >> 1
        temp+=1
    bin2set(led, leds)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(leds,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(troykaModule,GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comparator, GPIO.IN)

# ADC realisation, returns digital signal
def adc():
    signal = 128
    for value in range(8,0,-1):
        bin2set(signal, dac) 
#        voltage = maxVoltage * signal / levels
        time.sleep(period)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 0:
            signal -= 2**(value - 1)
        signal += 2**(value-1-1)
    signal-=1
    bin2set(signal, dac)
#    print("Digital value = {:^3}, Analog voltage = {:.2f} V".format(signal,voltage))
    ledPanel(signal)
    return signal

data = []
data_time = []

try:
    # Start of experiment
    GPIO.output(troykaModule, GPIO.HIGH)
    start = time.time()
    decline = False # Shows the moment condenser start to discharge
    print("Происходит зарядка конденсатора")
    while True:
        signal = adc()
        data_time.append(time.time()-start)
        data.append(signal)

        if signal > 255 * 0.95:
            GPIO.output(troykaModule, GPIO.LOW)
            decline = True
            print("Началась разрядка конденсатора")
        if decline and signal < 255*0.005:
            break
    
    # End of experiment
    end = time.time()
    print ("Experiment duration = {}, Period of measurement = {}, sample frequency = {:.2f}, шаг по напряжению = {:.2f}".format(end-start, period, 1/period, 1/levels*maxVoltage))
    
    # Graph
    plt.plot(data)
    plt.show()
    
    # File data
    data_str = []
    for i in range(len(data)):
        data_str.append("{}".format(data[i]))

    with open("data.txt", "w") as data_file:
        data_file.write("\n".join(data_str))
        data_file.close()
    with open("settings.txt", "w") as settings_file:
        settings_file.write("{:.3f} {:.2f}".format(end - start, maxVoltage * 1 / levels))
        settings_file.close()

except ArithmeticError:
    print("not")
finally:
    # initialization (back)
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    GPIO.output(troykaModule, GPIO.LOW)
    GPIO.cleanup(troykaModule)
    GPIO.cleanup(comparator)
    print("GPIO cleanup completed")