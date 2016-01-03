scenes = [
    ['You begin on your quest to get Larry-senpai to notice you! You are currently DJing a party where Larry-senpai is present. What music selection will you choose?', 'Rock n roll', 1, 'Smooth, smooth jazz', 2], #0
    ['You put on some old school rock n roll. Unfortunately, it seems like rock n roll is not what Larry-senpai wants to hear. He dances half-heartedly for a little while and leaves the party.', 'lose'], #1
    ['You put on some smooth, smooth jazz. Nice! Larry-senpai looks over in your direction. You can see that his dance moves are beginning to kick up a ruckus on the dance floor. What do you do?', 'Shout out Larry-senpai\'s name', 3, 'Blush furiously', 4], #2
    ['You yell out Larry-senpai\'s name into the crowd. Everyone gives you an awkward look, but Larry-senpai looks right at you and smiles and waves. What a nice guy.', 'win'], #3
    ['You blush furiously and continue to DJ. Nothing happens. Really, what did you expect that to do?', 'lose'] #4
    ]

def opening_scene():
    opening = ''
    with open('opening_scene.txt', 'r') as f:
        for line in f:
            opening += line
    print(opening)
    print()

def print_scene(scene):
    print(scene[0])
    print()
    print('1:', scene[1])
    print('2:', scene[3])
    print()

def get_choice(scene):
    choice = input('Enter your choice (1 or 2): ')
    while True:
        if choice.strip() == '1':
            return scene[2]
        elif choice.strip() == '2':
            return scene[4]
        else:
            choice = input('Please enter either 1 or 2: ')

def print_win(scene):
    print(scene[0])
    print()
    choice = input('Congratulations, Larry-senpai noticed you! You won! Play again (y/n)? ')
    while True:
        if choice.strip() == 'y' or choice.strip() == 'Y':
            return True
        elif choice.strip() == 'n' or choice.strip() == 'N':
            return False
        else:
            choice = input('Please enter either y or n: ')

def print_lose(scene):
    print(scene[0])
    print()
    choice = input('Oh no, Larry-senpai didn\'t notice you! Try again (y/n)? ')
    while True:
        if choice.strip() == 'y' or choice.strip() == 'Y':
            return True
        elif choice.strip() == 'n' or choice.strip() == 'N':
            return False
        else:
            choice = input('Please enter either y or n: ')

def begin_adventure():
    opening_scene()
    index = 0
    while True:
        scene = scenes[index]
        if scene[1] == 'win': # win condition
            restart = print_win(scene)
            if restart:
                begin_adventure()
            break
        elif scene[1] == 'lose': # lose condition
            restart = print_lose(scene)
            if restart:
                begin_adventure()
            break
        else:
            print_scene(scene)
            index = get_choice(scene)
            print()

begin_adventure()
