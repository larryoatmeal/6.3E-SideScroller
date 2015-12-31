'''
A complete beginner's intro to Python, using text adventure games.
By: Felix Sun (fephsun), for 6.3E IAP 2016.

Usage:
This file is designed to be an instructor's view.  When you are teaching a
class, you should have this file open in a window in the background (maybe even
another monitor) for reference and copy-pasting.

Part 1: Functions and variables
Code is made of lines, run in order from top to bottom.
The simplest thing a line can contain is a function.
Explain what a function is.
Explain the syntax.
'''

def part1_1():
    print(12)
    print('Hello world')
    # Remember to explain the syntax for strings.  Go really slowly here - you
    # should show what a syntax error looks like.
    print(4 + 7)
    print('Blah ' + 'more blah')

'''
Variables are just values that you can set and change in the code.
Mention that these are nothing like algebraic variables - this is really
confusing.
'''

def part1_2():
    # How to set a variable - name of variable on left, value on right.
    x = 4 + 5
    # How to use a variable - just drop the name in place
    print(x)

    # Does this work?  Why not?
    5 = x
    # What does this do?
    x = 4
    x = x + 3
    # This should make sense to you now:
    x = 12
    y = 7
    print(x + y)

'''
Some functions just do something, like print().  Other functions return a value
that your code can use.  (These are more like the functions you learned in
algebra.)
'''

def part1_3():
    y = abs(-6)
    print(y)
    # Explain what is going on when you say:
    print(abs(-6))  # (Call order of functions, etc.)

'''
One last function to discuss: getting user input.
'''

def part1_4():
    print('Enter your name:')
    user_name = input()
    print(user_name)
    # A few things to note: input() always returns a string.  Even if the user
    # types in a number, or nothing at all.  You can put a single parameter
    # into input() to add a prompt to that line.

'''
Now, you should try getting the user's name, and printing back "Hello <name>.
It's nice to meet you, <name>."

Hint: remember what the addition operator does on strings.
'''

