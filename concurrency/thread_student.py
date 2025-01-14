from threading import Thread

shared_variable = "original value"

def worker_thread():
   global shared_variable
   shared_variable = "new thread value"
   print("Hello from the worker thread")

if __name__ == "__main__":
    my_thread = Thread(target=worker_thread)
    my_thread.start()
    print("Hello from the main thread")
    my_thread.join() # wait for thread to finish
    print("Back to the main thread")
    print(shared_variable)
