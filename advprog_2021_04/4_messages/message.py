# message.py
#
# Introduction
# ------------
# Arjoon is working on a distributed system involving message passing.
# There are several components to the system including messages,
# dispatching, and message encoding.  However, our concern here is not
# so much the actual mechanics of the messaging (i.e., networks), but
# issues related to the organization and composition of the parts
# that will ultimately make up the system.

# -----------------------------------------------------------------------------
# Exercise 1 - This message will self destruct... probably
#
# In this messaging system, programs potentially run forever, creating
# billions of messages.  One area of concern is object management and
# garbage collection. How do messages get created?  When do they get destroyed?
# Is it possible for Python to "leak" memory, making it one of those
# programs that you have to restart every so often just to keep it from
# consuming every last bit of RAM on your computer?
#
# Python uses reference counting to manage the life-time of objects.
# The reference count is increased on an object whenever you make a
# new variable reference or store it in any kind of container.  The
# reference count is decreased when variables go away or the object is
# removed from a container.  Normally, it just "works" and you don't
# worry about it.
#
# The __del__() method, if defined on an object, is called when the
# reference count of an object has reached zero and it's about to be
# destroyed.  It's hardly ever necessary to define this because Python
# will properly clean up even you do nothing.  However, doing so can
# be instructive to learn more about how Python works.
#
# Consider the following Message class.  This class represents the
# basic components of a "Message" Arjoon's distributed system. The
# "source" and "dest" attributes are addresses.  An internal,
# always incrementing, sequence number is also attached to the message.
# The purpose of the sequence number is to help with things like
# timing, dropped messages, duplicate messages, etc (e.g., a receiver
# could detect a missing message by noting a gap in sequence numbers).

class Message:
    _sequence = 0

    def __init__(self, source, dest, payload, sequence=None):
        self.source = source
        self.dest = dest
        self.payload = payload
        if sequence is None:
            self.sequence = Message._sequence
            Message._sequence += 1
        self.sequence = sequence

    def __repr__(self):
        return f'Message<{self.sequence}: source={self.source}, dest={self.dest}>'

    def __del__(self):
        print(f'Message {self.sequence} destroyed')

# Try a quick interactive example of creating and destroying a message.
#   
#    >>> m = Message(0, 1)
#    >>> del m
#    Message 0 destroyed
#    >>>
#
# Does a message get destroyed if you forget to call del and simply
# reassign the "m" variable instead?
#
#    >>> m = Message(0, 1)
#    >>> m = Message(2, 3)    # What happens to previous message?
#
# Inside the "__del__" method, nothing happens except a print
# statement.   Does it matter than __del__() doesn't do anything
# with the "source", "dest", or "sequence" attributes?
#
# Try this experiment:
#
#    >>> class Address:
#            def __init__(self, n):
#                self.n = n
#            def __del__(self):
#                print(f"Destroying Address {self.n}")
#
#    >>> m = Message(Address(0), Address(1))
#    >>> del m
#    ... watch what happens ...
#
# You should see the Address objects being destroyed automatically. This,
# despite the fact that the Message.__del__ method doesn't actually do
# anything to make it happen.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Exercise 2 - The Construction
#
# One weird thing about the Message class is that the sequence number is
# set implicitly based on the value of Message._sequence.  In this case,
# Message._sequence is a "class variable."  It exists in only one place
# and functions kind of like a global variable.
#
# Suppose you wanted to construct a Message with a very specific sequence
# number instead of the one that's set automatically?   How would you do that?

def test_construction():
    d = { 'source': 0, 'dest': 1, 'payload': 'Hey', 'sequence': 1234 }
    orig_sequence = Message._sequence

    # This doesn't work. You need to fix it.  How?!?
    m = Message(d['source'], d['dest'], d['payload'], d['sequence'])

    assert m.source == 0
    assert m.dest == 1
    assert m.sequence == 1234
    assert Message._sequence == orig_sequence   # Unchanged

# Uncomment
test_construction()

# -----------------------------------------------------------------------------
# Exercise 3 - The Game
#
# Suppose that this messaging system was going to be used to implement
# a game and there different types of game messages--each holding
# different information (i.e., chat messages, player updates, player
# actions, etc.).  For example (in psuedocode):
#
#    ChatMessage {
#        player_id : int    # Player id sending message
#        text : str         # Message contents (UTF-8 Text)
#    }
#
#    PlayerUpdate {
#        player_id : int    # Player being updated
#        x : float          # New x position
#        y : float          # New y position
#    }
#
# How would you implement these different message types in relation to the
# Message class above?   For example, is inheritance involved? Or
# is it more of a composition problem?
#
# You're the system designer:  Define Python classes for the above messages.
# And show how a message instance of each type would be created.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Exercise 4 - Message on a Wire
#
# In order to send a message someplace, it needs to be serialized into
# a stream of bytes and deserialized from bytes back into a Message
# instance.  Assume that there's supposed to be some kind of "encode"
# operation that takes a Message and turns it into bytes and a
# "decode" operation takes bytes and turns them back into a Message.
#
# Design Challenge: How would you structure/write code to handle the
# message encoding/decoding problem with the following design
# considerations:
#
# - There are might be dozens of different game message types, each
#   with different data fields
# - There are many possible low-level message encodings (pickle, 
#   JSON, XML, etc.).  These encodings might be hooked to other
#   programming languages.  They might involve binary data. They
#   might NOT be Python-specific (like Pickle) or based on passing
#   dictionaries around (like JSON).
# - It might be necessary to implement a new encoding in the future.
#
# Note: This is a fairly open-ended problem that is fraught with peril.
# To start out, you might try using Python's "pickle" module.
#
#     import pickle
#     raw = pickle.dumps(msg)    # Message -> bytes
#     msg = pickle.loads(raw)    # bytes -> Message
#
# Then switch over to using JSON encoding Python's json module.  Keep
# in mind this is more of a design problem--we want to be able to
# deal with different encodings, message types, etc.
# -----------------------------------------------------------------------------


import pickle

def encode(message):
    raw = pickle.dumps(message)
    return raw

def decode(raw_message):
    msg = pickle.loads(raw_message)
    return msg



# The following "test" illustrates the basic requirements of encoding/decoding
def test_serial():
    m1 = Message(0, 1, 123, "Test Message")  # This might vary depending on (2) above
    print(f'this is the original message: {m1}')
    # You need to figure out the "encode" operation.  It can look different
    # than what's shown, but the final result must be bytes.
    raw = encode(m1)
    print(f'This is raw message: {raw}')
    # The encoded message (whatever it is) must be bytes. Something that
    # can be transmitted somewhere else.
    assert isinstance(raw, bytes)

    # The decode operation must accept bytes and recreate a message.
    # Again, this can look different than what's shown.  However, the
    # final result must be identical to the original message.
    m2 = decode(raw)
    print(f'This is decoded message: {m2}')
    assert isinstance(m2, Message)   # Might need to adjust depending on Exercise 3.

    # The final message must be identical to the original message in
    # every way.  This includes the dest, source, sequence numbers,
    # payload, and everything.  You might need to add methods to
    # make messages comparable or change this code in some way to
    # make the assert pass
    print(f'm1: {m1}')
    print(f'm2: {m2}')
    assert m1 == m2

# Uncomment
test_serial()

# -----------------------------------------------------------------------------
# Exercise 5 - There can be only one
#
# To send messages, Arjoon has decided on an architecture where all
# messages are given to a central Dispatcher object. Its primary
# method is send().  You provide a message to the Dispatcher and it
# takes care of delivering it to a proper location.
#
# The actual implementation details of the Dispatcher delivery process
# are left somewhat vague. This is by design.  Yes, there is a send()
# method, but the internal implementation of could be almost anything.
# We just don't know.  We're not really supposed to know.  It's like
# the post office--you drop off a letter and what happens beyond that
# is not our problem.
#
# With that in mind, here is a new problem involving the Dispatcher.
#
# 1. An instance of some kind of Dispatcher class must 
#    be created in the application.  
#   
# 2. That instance must implement the required send() method.
#
# 3. There can only be ONE instance of a Dispatcher object created 
#    in the entire program (i.e., a "Singleton")
#
# 4. There must be some way for code to easily obtain a reference 
#    to the ONE Dispatcher instance. 
#
# Your challenge: Implement this.
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod

class Dispatcher(ABC):
    '''
    Base class.  Do not create instances of this. Use a subclass.
    '''
    @abstractmethod
    def send(self, msg):
        pass

# Example of a child-class that simply prints messages.
class SimpleDispatcher(Dispatcher):
    def send(self, msg):
        print('Sending:', msg)

# There must be some way to obtain/access the dispatcher object from 
# any other code. Is getting the dispatcher the same as creating one?
# What is the programming interface for this?
def test_send():
    d = ...                 # get the one true dispatcher somehow
    d.send("Hello World")   # Send a message of some sort

# Uncomment
# test_send()

# Thought:  How do you ensure that there is only one Dispatcher?

# -----------------------------------------------------------------------------
# Exercise 6 - The Unsubscribe Problem
#
# Arjoon has decided to implement a dispatcher based on the idea of
# publish/subscribe.  The general idea is that different handlers can
# subscribe to a specific message destination address. Any message
# sent to that address will be given to the handler.  If multiple
# handlers are subscribed to the same address, each handler will
# receive all of the messages.  Here's an example of a Dispatcher that
# implements this general idea.

from collections import defaultdict

class PubSubDispatcher:
    def __init__(self):
        self.subscribers = defaultdict(set)

    def subscribe(self, addr, handler):
        self.subscribers[addr].add(handler)

    def send(self, msg):
        for handler in self.subscribers[msg.dest]:
            handler.receive_message(msg)

# An example of of handler that receives messages
class ExampleHandler:
    def __init__(self, name):
        self.name = name

    def receive_message(self, msg):
        print(f'{self.name} got', msg)

# An example of using using the dispatcher and subscribing a handler
def pubsub_example():
    dispatcher = PubSubDispatcher()
    # Create some handlers
    h1 = ExampleHandler("Handler1")
    h2 = ExampleHandler("Handler2")
    dispatcher.subscribe(0, h1)       # h1 subscribed to channel 0
    dispatcher.subscribe(1, h2)       # h2 subscribed to channel 1
    dispatcher.subscribe(1, h1)       # h1 additionally subscribed to channel 1
    dispatcher.send(Message(0, 1))    # Message from 0 -> 1   
    dispatcher.send(Message(1, 0))    # Message from 1 -> 0

# Uncomment to try it.  Make sure you understand what's happening above.
# pubsub_example()

# THE DEBATE:
# ===========
#
# The above dispatcher is simple enough, but a debate has erupted over
# the proper way to *unsubscribe* handlers from the
# dispatcher. Basically, the problem relates to the lifetime of the
# handler objects themselves.  When no longer needed, it should be
# possible to detach the handler from the dispatcher in some way.
#
# Option 1:  Explicit Unsubscribe.
# --------------------------------
# Arjoon thinks that a simple solution to this problem is to implement
# an explicit "unsubscribe()" method that takes the same arguments
# as subscribe().  You use it like this:
#
#     dispatcher.subscribe(channel, handler)
#     ...
#     dispatcher.unsubscribe(channel, handler)
#
# "It's straightforward. It's easy", he argues.
#
# Option 2:  Unsubscribe on Garbage Collection
# --------------------------------------------
# Mel thinks that handlers should automatically unsubscribe themselves
# when they go out of scope and are garbage collected.  She's proposed
# a different kind of function "watch()" that works like this:
#
#      handler = ExampleHandler()
#      dispatcher.watch(channel, handler)
#      ...
#      del handler         # Handler is automatically unsubscribed.
#
# "You don't have to worry about it", she argues.
#
# Option 3: Unsubscribe with a Context Manager
# --------------------------------------------
# Python supports a feature known as a "context manager" that's
# often used to define a scope/lifetime in which an object is used.
# You've used it if you've ever used the "with" statement in
# combination with a file, a lock, or some other resource.
#
# Michelle thinks that all of this could be refined by introducing the
# idea of a dispatcher context.  You'd use it like this:
#
#     with dispatcher as context:
#         handler = ExampleHandler()
#         context.subscribe(channel, handler)
#         ...
#     # All handlers in the context automatically unsubscribed
#
# YOUR CHALLENGE:
# ---------------
# Modify the PubSubDispatcher class so that it supports *ALL THREE* of
# the above subscribe/unsubscribe approaches.
#
# The following tests will verify that it's working.  Note: You
# should be able to pass all three tests at once.

class TestHandler:
    def __init__(self, name, maxuse):
        self.name = name
        self.maxuse = maxuse
        
    def receive_message(self, msg):
        assert self.maxuse > 0, "Why did I receive this?"
        print(f'{self.name} got', msg)
        self.maxuse -= 1

# Option 1: Explicit unsubscribe
def test_option1():
    dispatcher = PubSubDispatcher()
    h1 = TestHandler("Handler1", 1)
    dispatcher.subscribe(1, h1)
    dispatcher.send(Message(0, 1))
    dispatcher.unsubscribe(1, h1)
    dispatcher.send(Message(0, 1))    # Handler should not receive this
    print("Good unsubscribe")

# test_option1()            # Uncomment

# Option 2:
def test_option2():
    dispatcher = PubSubDispatcher()
    h2 = TestHandler("Handler2", 1)
    dispatcher.watch(1, h2)
    dispatcher.send(Message(0, 1))
    del h2
    dispatcher.send(Message(0, 1))    # Handler should not receive
    print("Good watching")

# test_option2()           # Uncomment

# Option 3:
def test_option3():
    dispatcher = PubSubDispatcher()
    with dispatcher as context:
        h2 = TestHandler("Handler3", 1)
        context.subscribe(1, h2)
        dispatcher.send(Message(0, 1))
        
    dispatcher.send(Message(0, 1))    # Handler should not receive
    print("Good context manager")

# test_option3()          # Uncomment

    
        
    
