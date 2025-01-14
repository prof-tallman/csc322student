
# Prof Tallman
# 
# Simple demos are just a little tougher to show in python than in C because
# the Python Interpreter's Global Interpreter Lock (GIL) artificially limits 
# python bytecode from being executed concurrently. Credit to Dr. Jason
# Brownlee and several Stackoverflow users who explained some of the nuances
# of the GIL and how we can still create race conditions.
#
# https://superfastpython.com/thread-race-condition-shared-variable/#Example_of_Race_Condition_in_Python_310
# https://superfastpython.com/multiprocessing-race-condition-python/
# https://stackoverflow.com/questions/52507601/whats-the-point-of-multithreading-in-python-if-the-gil-exists
# https://stackoverflow.com/questions/68847492/python-multi-threading-race-condition-behavior-changes-as-a-function-of-time
# https://docs.python.org/3/glossary.html#term-global-interpreter-lock

from threading import Thread, Lock
from time import sleep

# Poorly protect shared variable
my_lock = Lock()
x = 0

def increment():
    """
    Increments a global variable in a way that is vulnerable to race
    conditions and is likely to produce the wrong result.
    """
    # Although this code *appears* to be sabotaged in an unrealistic way, the
    # multi-step process is exactly what happens at the machine code level.
    # A variable is taken from memory and loaded into a register. The register
    # is incremented and then the result is stored back to memory. We had to
    # divide the sequence into multiple steps because python has artificial
    # protection against simple errors like this in the form of a GIL - Global 
    # Interpreter Lock. However, the GIL is unable to protect against the same
    # race conditions in complex code... but complex demos are hard to follow.
    global x
    global my_lock
    with my_lock:
        tmp = x
        tmp = tmp + 1
        sleep(0)
        x = tmp


def increment_100_times():
    """
    Increments a variable 100 times in a row.
    """
    for _ in range(100):
        increment()

def main():
    """
    Two threads increment a shared variable 100 times each, for an expected
    total count of 200. 
    """
    
    # initialize counter to zero
    global x
    x = 0

    # start two counting threads
    t1 = Thread(target=increment_100_times)
    t2 = Thread(target=increment_100_times)
    t1.start()
    t2.start()

    # wait for both threads to finish, then print result
    t1.join()
    t2.join()

    print(f'Iteration {i}: x={x}')
    return

if __name__ == '__main__':
    for i in range(10):
        main()
