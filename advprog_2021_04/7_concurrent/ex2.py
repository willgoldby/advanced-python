# -----------------------------------------------------------------------------
# Exercise 2 - Sleeping
#
# Consider the original code again...

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

# -----------------------------------------------------------------------------
# THE SLEEPING PROBLEM
#
# In the above code, there are calls to time.sleep().   These are long-running
# calls that block the execution of everything else.  Your task is to reimplement
# the functionality of time.sleep() so that multiple functions can be sleeping
# at the same time and run at different rates.  Specifically, you want the
# output to look something like this where the countdown process is producing
# three times as much output, but both functions finish at the same time.
#
# T-minus 15
# Up we go 0
# T-minus 14
# T-minus 13
# T-minus 12
# Up we go 1
# T-minus 11
# T-minus 10
# T-minus 9
# Up we go 2
# T-minus 8
# T-minus 7
# T-minus 6
# Up we go 3
# T-minus 5
# T-minus 4
# T-minus 3
# Up we go 4
# T-minus 2
# T-minus 1

# ---- Paste in your code from Exercise 1 and modify it to solve
# ---- the sleeping problem.

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
