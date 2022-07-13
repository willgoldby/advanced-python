# -----------------------------------------------------------------------------
# Exercise 4
#
# "Oh my, it's full of fail."
#
# One somewhat subtle thing about after() is that it runs a function
# on your behalf and returns its result. Carefully study and ponder
# the following two edge cases, both of which fail:
#
#     after("10", lambda: add(2, 3))      # Case 1
#     after(10, lambda: add("2", 3))      # Case 2
#
# One of these is not like the other.  But, what is different about it?
# Spend a few minutes to ponder the output and to understand what is
# happening here. Both examples result in the same kind of exception,
# but is it really the same kind of failure?
# 
# Your task: Can you redesign the after() function in a way that more
# clearly separates exception handling into two categories of
# failures--errors that are caused by bad usage of the after() function
# itself versus errors that get raised by the supplied function (func).
#
# Hint: One way to organize exceptions is to define and use a custom exception.
# -----------------------------------------------------------------------------

import time

class AddException(Exception):

    @staticmethod
    def bad_arguments():
        print('You used bad arguments.')

    @staticmethod
    def bad_result():
        print('Your logic is bad.')


def after(seconds, func):
    try:
        time.sleep(seconds)
        return func()
    except:
        AddException.bad_arguments()

def add(x, y):
    try:
        print(f'Adding {x} + {y} -> {x + y}')
        return x + y
    except:
        AddException.bad_result()
        
after("10", lambda: add(2, 3))
after(10, lambda: add("2", 3))

# Again, your task: Can you make the second call to after() produce a different
# kind of exception to distinguish it from the failure that occurs
# in the first call?
