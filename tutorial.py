'''
A complete beginner's intro to Python.
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
    y = x
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

'''
Part 2: Working with lists and strings
Explain syntax for creating and accessing lists.
Explain casting types and explore some other types of errors.
Share some handy string functions.
'''

'''
You can also make lists of things, including variables.
'''

def part2_1():
    # Create a list that contains the numbers 1, 2, and 3:
    print([1, 2, 3])
    # You can make lists of strings, too:
    print(['cat', 'pictures'])
    # In Python, you can mix and match different types of things in your list:
    print([1, 'fish', 2, 'fish', 'red', 'fish', 'blue', 'fish'])
    # You can even put variables in a list, or other lists too
    x = 1
    y = [x, 2]
    print(y)
    z = [y, 3]
    print(z)
    # Here's how you access the things in a list. If I want the first element of
    # the list, I ask for the element at index 0, and so on:
    x = ['first', 'second', 'third']
    print('The first element of x:', x[0])
    print('The second element of x:', x[1])
    print('The third element of x:', x[2])
    print('The last element of x:', x[-1])
    print('The second-to-last element of x:', x[-2])
    # You can get several elements by picking a range of indices in the list.
    # For example, x[0:2] gets the elements at index 0 through 2 (including 0,
    # but not including 2).
    print('The first and second elements of x:', x[0:2])

'''
You can do the same kind of indexing in a string, too. Try getting the first and
last names of a user, and then printing out their initials. Here's some stuff to
get you started.
'''

def part2_2():
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    initials = '<replace this!>'
    print('Your initials are:', initials)

'''
Now let's try to do something useful(ish). Here's some code that is designed to
square a number given by the user.
'''

def part2_3():
    number = input('Enter the number to square: ')
    # Uh oh! We run into an error here.
    print('The number squared is', number * number)

'''
What went wrong? We got an error: it looks like we tried to multiply something
that we couldn't multiply. But wait, weren't we just trying to multiply two
numbers? It turns out that the value of number was actually a string, not a
number! To multiply it properly we need to convert it to a number, using some
more functions.
'''

def part2_4():
    number = input('Enter the number to square: ')
    # This converts the number from a string to an integer, which cuts it down
    # to the nearest integer:
    number = int(number)
    # If we wanted to include decimal places too, we can convert a string to
    # a type of number called a float:
    pi = float('3.14')
    print('The number squared is', number * number)
    # What if a user enters something bogus, like "Larry"? Obviously we can't
    # convert "Larry" to a number.
    not_actually_a_number = int('Larry')
    # Typing out "number*number" is a huge pain. Since we're squaring things,
    # why don't we do "number^2"?
    number = 4
    print('4 squared is', number ^ 2, '...or is it?')
    # Whoa, that's not what we expected. 4^2 is definitely 16, not 6. What
    # happened? Turns out that the caret operator ^ actually does something
    # else -- a bitwise OR, if that means anything to you. If it doesn't, no
    # sweat, you probably won't ever use it. The way to raise something to a
    # power in Python is with the ** operator:
    print('4 squared is', number ** 2)
    print('4 cubed is', number ** 3)

'''
Here's some handy functions to use with strings: split() and strip().
'''

def part2_5():
    # You can use split() to split up a string into a list of strings.
    sentence = 'This is a string.'
    print(sentence)
    print(sentence.split())
    # You can use strip() to get rid of "trailing" whitespace: things like
    # spaces and tabs at the beginning and end of the string. By the way, the \t
    # means a tab. (Don't use the tab on your keyboard if you're trying to put a
    # tab in a string.)
    sentence = '          \tThis is a sentence with a lot of spaces.   '
    print(sentence)
    print(sentence.strip())

'''
Part 3: Control flow
ifs, elses, whiles, and fors
'''

