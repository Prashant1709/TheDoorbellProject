import RPi.GPIO as GPIO
import time
import threading
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
def btn1():
	while True:
		if GPIO.input(23):
			print("Button UnPressed")
			time.sleep(0.2)
		else:
			print("Button pressed")
			os.system('python3 facial_req_email.py')

def main():
	thread1=threading.Thread(target=btn1)
	thread1.start()


if __name__=='__main__':
	main()
