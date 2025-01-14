from multiprocessing import Process

shared_variable = "original value"

def worker_process():
   global shared_variable
   shared_variable = "new proces value"
   print("Hello from the worker process")

if __name__ == "__main__":
    my_process = Process(target=worker_process)
    my_process.start()
    print("Hello from the main process")
    my_process.join() # wait for process to finish
    print("Back to the main program")
    print(shared_variable)
