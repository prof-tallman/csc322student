from threading import Thread
from time import sleep

shared_variable = "original value"

def worker_thread():
    global shared_variable
    sleep(0.0001)
    shared_variable = "new thread value"
    print("Hello from the worker thread")
    for i in range(10000):
       sleep(0.0001)
    print("Done sleeping")

if __name__ == "__main__":
    my_thread = Thread(target=worker_thread)
    my_thread.start()
    for i in range(10):
        print("Hello from the main thread")
        sleep(0.0001)

    my_thread.join() # wait for thread to finish
    print("Back to the main thread")
    print(shared_variable)
