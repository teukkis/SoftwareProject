from time import sleep
import signal

def handler(signum, frame):
    if signum == 1:
        print("Good try")
signal.signal(1, handler)
signal.signal(signal.SIGTSTP,handler)
while True:
    try:
        print("asd")
        sleep(1)
    except:
        print("Catched interrupt")