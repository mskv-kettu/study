import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pair = [22, 10]
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

p = GPIO.PWM(22, 1000)
p1 = GPIO.PWM(10, 1000)
p.start(0)
p1.start(0)
try:
    while 1:
        inputStr = input("Enter a value between 0 and 100 ('q' to exit) > ")
        if inputStr.isdigit():
            cd = int(inputStr)
            p.ChangeDutyCycle(cd)
            p1.ChangeDutyCycle(cd)
        else:
            print("invalid value")
            continue
       
except KeyboardInterrupt:
    pass
finally:
    p.stop()
    GPIO.cleanup()