# -----------------------------------------------------------------------------
# Exercise 5
#
# The "Box".  One challenge in returning results is that there are
# actually two kinds of results from any Python function--a value
# returned by the "return" statement or an exception raised by the
# "raise" statement.  One possible design for programs that submit
# function evaluation as "work" is to place both possible results
# inside a combined Result object that gets used like this:
#
#     result = after(10, func)     # Always returns a result
# 
# Once you have the result, you "unwrap" it to get the actual outcome:
#
#   try:
#       value = result.unwrap()
#   except Exception as e:
#       print("An error occurred")
#
# Sometimes this approach is known as "boxing."  That is, the result
# gets stuffed into a box.  You don't know what it is until you open
# the box.  It's like a birthday present.
#
# Your task: Implement a Result class that allows results to be returned in
# exactly the manner as shown above.  Modify the after() function to return
# a Result instance.  
# -----------------------------------------------------------------------------
import time

class Result:
    def __init__(self, value=None, err=None):
        self.value = value
        self.err = err

    def unwrap(self):
        # Return the actual result or raise an exception
        if self.err:
            raise self.err
        else:
            return self.value

def after(seconds:float, func) -> Result:
    time.sleep(seconds)
    try:
        return Result(value=func())
    except Exception as err:
        return Result(err=err)

# Example
def add(x, y):
    print(f'Adding {x} + {y} -> {x + y}')
    return x + y

if __name__ == '__main__':
    r = after(5, lambda: add(2, 3))
    assert r.unwrap() == 5

    r = after(5, lambda: add('2', 3))
    try:
        a = r.unwrap()
        print('Bad! Why did this work?')
    except TypeError as err:
        print('Good!')

