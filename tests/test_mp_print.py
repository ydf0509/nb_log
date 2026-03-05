

from multiprocessing import Process
import time
import nb_log

def print_hello():
    while True:
        print("Hello, World!")
        time.sleep(1)

if __name__ == "__main__":
    print('start')
    p = Process(target=print_hello)
    p.start()
    p.join()

