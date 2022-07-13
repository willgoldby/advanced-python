# -----------------------------------------------------------------------------
# Exercise 1 - Concurrency
#
# Consider the following two functions.

import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        time.sleep(1)
        n -= 1

def countup(stop):
    x = 0
    while x < stop:
        print('Up we go', x)
        time.sleep(3)
        x += 1

# Normally, functions execute sequentially--meaning one after the
# other.  For example, observe the output of the following code.

countdown(15)
countup(5)

# -----------------------------------------------------------------------------
# YOUR TASK:
#
# Figure out a way for both of the above functions to execute
# concurrently, producing interleaved output like this:
#
#    T-minus 15      (1 sec delay)
#    Up we go 0      (3 sec delay)
#    T-minus 14      (1 sec delay)
#    Up we go 1      (3 sec delay)
#    T-minus 13
#    Up we go 2
#    T-minus 12
#    Up we go 3
#    T-minus 11
#    Up we go 4
#    T-minus 10
#    T-minus 9
#    T-minus 8
#    ...
#    T-minus 1
#
# THE CATCH: You are not allowed import any outside module to do it.
# Moreover, you're not allowed to use any feature of Python other than
# ordinary function calls.  That means no threading, no subprocesses,
# no async, no generators, or anything else. You need to figure out
# how to get something resembling concurrency to work all on your own
# without the support of any library.
# 
# You ARE allowed to change the implementation of the original functions
# and to write any other supporting code you might need to do it--as
# long as that support code only involves normal Python functions.

import time

def countdown(n):
    #---- This is a single step
    print('T-minus', n)
    time.sleep(1)
    # ----
    # This is the next step.
    if n > 0:
        call_soon(lambda: countdown(n-1))   # Doesn't run right now. Just puts on the list

def countup(stop):
    # The problem here.... how does one track the "x"?   It has to be carried forward to the next step.
    # One possibility... make it an argument.   Another option.  Make a helper function.
    def helper(x):
        print('Up we go', x)
        time.sleep(3)       # NO BLOCKING
        if x < stop:
            call_soon(lambda: helper(x+1))

    # Start the calculation
    helper(0)

# Adaption of the idea from project 6
ready = [ ]       # Functions that can be called

def call_soon(func):
    ready.append(func)

def run():
    while ready:
        func = ready.pop(0)
        func()

call_soon(lambda: countdown(15))
call_soon(lambda: countup(5))
run()
