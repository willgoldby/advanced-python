# -----------------------------------------------------------------------------
# elevator.py
#
# Certain problems often involve the implementation of "state
# machines."  For example, consider the operation of an elevator.  At
# any given moment, the elevator is in a certain "operational state".
# For example, it's positioned at a given floor and it's either
# idle, loading passengers, or moving. The doors are open or closed.
# The elevator transitions between states according to various events
# which may include buttons, sensors, and timers.
#
# Suppose that you are tasked with designing and writing the control
# software for an elevator in a 5-floor building.   The elevator has
# the following inputs:
#
#  1. A push button inside the elevator to select a destination floor.
#  2. Two push buttons (up/down) on each floor to request the elevator.
#  3. A sensor on each floor to indicate the current elevator position 
#     (triggered when the elevator reaches a given floor).
#  4. A time-expired event that's used for time-related operation.
#
# The elevator has the following control outputs:
#
#  1. Hoist motor control (controls up/down motion)
#  2. Door motor control (controls door open/close motion)
#  3. Set a timer.
#
# The elevator operates in three primary operational modes.
#
# 1. IDLE: The elevator remains still if there are no floor requests.  
#    This means it's just stopped on whatever floor it happened to
#    go to last with the doors closed.  Any request causes
#    the elevator to start moving towards that floor.
#    
# 2. MOVING: The elevator is in motion. Once in motion, the
#    elevator continues to move in its current direction until
#    it reaches the highest or lowest requested floor.  Along
#    the way, the elevator will serve other requests as appropriate.
#    For example, suppose the elevator is on floor 1 and someone
#    hits the "down" button on floor 4.  The elevator will start
#    moving up.  If, on the way up, someone presses "up" on 
#    floor 3, the elevator will stop and load passengers before
#    continuing up to floor 4.  If someone also pressed "down" on
#    floor 5, the elevator would *pass* floor 4 and go up to
#    floor 5 first.  It would then stop on floor 4 on its way
#    back down. 
#
# 3. LOADING: When stopped at a floor, the door opens for 10 seconds
#    and then closes again.  There is no mechanism to make the door
#    stay open.  Anything in the way gets cut in half--an obvious
#    limitation to be addressed in a future version.
#
# YOUR TASK: Design and implement code for the internal logic and
# control of the elevator.  Come up with some strategy for testing it.
#
# CHALLENGE: To write this code you might ask to know more about how
# the elevator control actually works (i.e., How are inputs delivered?
# How is data encoded?  How are commands issued to the motors?). How
# does the elevator deal with acceleration and deceleration. However,
# you're not going to get it. That's a different corporate division.
# So, you've got to figure out how to implement the elevator control
# software without any first-hand knowledge of its deployment
# environment or the laws of physics.  Naturally, the lack of
# information means that your implementation will need to be
# extended/embedded in some other software (not shown/provided) to be
# used in the real world.  It also means that your understanding
# of the problem might be incomplete--you should write the code
# in anticipation of new unforeseen "requirements."
# -----------------------------------------------------------------------------

# A Hint: It might make sense to separate the problem into separate
# concerns.  For example, perhaps you define an "Elevator" class that
# deals with the logic of the elevator and a "ElevatorControl" class
# that is focused on its interaction with "real" world elements.  For
# example:


HIGHEST_FLOOR = 5

class ElevatorCar:

    def __init__(self, mode='IDLE', floor=1, direction=None, requests=None):
        # Operational mode (IDLE, LOADING, MOVING)
        self.mode = 'IDLE'

        # Current floor where the elevator is positioned.
        self.floor = floor

        # Current direction of motion (if any).
        self.direction = direction

        # Requested floors (buttons pressed inside the elevator car)
        self.requests = set() if requests is None else requests 

        # Validate the initial state
        self.validate()
    
    def __repr__(self):
        return f'ElevatorCar({self.mode}, {self.floor}, {self.direction}, {self.requests})'
    
    def validate(self):
        assert self.floor >= 1 and self.floor <= HIGHEST_FLOOR
        assert not (self.floor == 1 and self.direction == 'DOWN')
        assert not (self.floor == HIGHEST_FLOOR and self.direction == 'UP')
        assert not (self.mode == 'IDLE' and self.requests)


class CarState:

    @staticmethod
    def enter(car, manager, control):
        raise NotImplementedError


    # These are events that only pertain to cars.
    @staticmethod
    def destination_button_pressed(car, floor, manager, control):
        raise NotImplementedError()

    @staticmethod
    def floor_sensor(car, floor, manager, control):
        raise NotImplementedError()

    @staticmethod
    def timer_expired(car, manager, control):
        raise NotImplementedError()
    

# Nothing is happening
class CarIdle(CarState):
    @staticmethod
    def enter(car, manager, control):
        ...
    
    @staticmethod
    def destination_button_pressed(car, floor, manager, control):
        ...


# Car is moving upwards
class CarMovingUp(CarState):
    @staticmethod
    def enter(car, manager, control):
        ...
    @staticmethod
    def destination_button_pressed(car, floor, manager, control):
        ...
    
    @staticmethod
    def floor_sensor(car, floor, manager, control):
        ...

# Car is loading up moving upwards afterwards
class CarLoadingDown(CarState):
    @staticmethod
    def enter(car, manager, control):
        ...

    @staticmethod
    def destination_button_pressed(car, floor, manager, control):
        ...
    
    @staticmethod
    def timer_expired(car, manager, control):


class ElevatorManager:
    # Good idea: Make ALL state settable via optional arguments to __init__().
    # This lets you create an object in an arbitrary state (maybe useful for testing)
    def __init__(self, cars=None, down_requests=None, up_requests=None):
        
        # Elevator cars (There could be more than one).
        self.cars = [ ElevatorCar() ] if cars is None else cars
    
        # "Down" buttons pressed out in the hallway.
        self.down_requests = set() if down_requests is None else down_requests

        # "Up" buttons pressed out in the hallway.
        self.up_requests = set() if up_requests is None else up_requests

    def __repr__(self):
        return f'ElevatorManager({self.cars}, {self.down_requests}, {self.up_requests})'

    # Events that drive the elevator systems
    def destination_button_pressed(self, car_number, floor, control):
        # A button was pressed inside the elevator car.
        self.cars[car_number].requests.add(floor)

    def down_button_pressed(self, floor, control):
        # A 'down' button was pressed outside in the hallway.
        # control.hoist_motor('up')
        pass

    def up_button_pressed(self, floor, control):
        #An 'up' button was presssed out in the hallway.
        pass

    def floor_sensor(self, car_number, floor, control):
        # The moving elevator car trips a floor sensor.
        pass

    def timer_expired(self, car_number, control):
        # A timer expired. For example, after loading passengers for 10 seconds. 
        pass


class MockElevatorControl:
    
    def __init__(self, motor=None, door=None, timer=None):
        # Track information about motor, door, and timer for each car.
        self.motor = {} if motor is None else motor
        self.door = {} if door is None else door
        self.timer = {} if timer is None else timer
    
    def __repr__(self):
        return f'MockElevatorControl(motor={self.motor}, door={self.door}, timer={self.timer})'
    
    def hoist_motor(self, command):
        # Turn on the hoist motor for a given elevator car.
        # Command is 'up', 'down', 'off'
        # print("hoist", car_number, command)
        self.motor[car_number] = command

    def door_control(self, command):
        # Control the doors of an elevator car.
        # Command is 'close', 'open'.
        # print("door", car_number, command)
        self.door[car_number] = command

    def set_timer(self, seconds):
        # Set a timer. For example, the loading time.
        # Seconds is a positive number or None to reset/cancel.
        # print("timer", car_number, seconds)
        self.timer[car_number] = seconds


def test_example():
    manager = ElevatorManager()
    control = MockElevatorControl()

    # Test example:
    # Elevator is idel. On floor 1.
    # Down button pressed on floor 3 (in hallway)
    # What happens?
    # 1. Elevator starts moving up.

    manager.down_button_pressed(floor=3, control=control) # Event
    
    assert manager.cars[0].mode == 'MOVING'
    assert manager.cars[0].direction == 'UP'
    assert 3 in manager.down_requests
    assert control.motor[0] == 'up'

    # How does the elevator move? you want an 'event loop', but you don't get it!
    # Answer: Fake it.
    manager.floor_sensor(car_number=0, floor=2, control=control)
    manager.floor_sensor(car_number=0, floor=3, control=control)
    # More assertions. What happens on floor 3?
    # 1. Elevator stops. Doors open. etc...

    print("Good elevator!")

test_example()


# You don't have to follow this exact code pattern if you have
# something else in mind.

# -----------------------------------------------------------------------------
# Testing
#
# How do you test something like this?  See the file testing.py when you're
# ready.

