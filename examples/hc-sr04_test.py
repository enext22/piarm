import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 12
GPIO_ECHO = 11

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
  GPIO.output(GPIO_TRIGGER, True)

  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

  startTime = time.time()
  arrivalTime = time.time()

  while GPIO.input(GPIO_ECHO) == 0:
    startTime = time.time()

  while GPIO.input(GPIO_ECHO) == 1:
    arrivalTime = time.time()

  dist = ((arrivalTime-startTime)*34300)/2

  return dist

if __name__ == '__main__':
  try:
    while True:
      dist = distance()
      print(f"Measured distance = {dist} cm")
      time.sleep(1)
  except KeyboardInterrupt:
      print("Measurement stopped by user")
      GPIO.cleanup()
