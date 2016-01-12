# 6.3E-SideScroller
We will be using Python3 and PyGame 1.9.2 (not Python2 and PyGame 1.9.1 due to compatibility issues with El Capitan) 

Read through this for installation instructions (not the PyGame site)
http://programarcadegames.com/index.php?chapter=foreword&lang=en#section_0

# Notes
##Windows 
Installation is relatively straightforward. Just make sure you're using Python3 when you're executing the scripts. You may have to play with the environmental variables to make sure Python3 is in your path. 
http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7 (follow this, but use the python3 installation folder instead)
If you already have Python2 installed, I recommend renaming the python executable to python3.

##Mac 
Installation is a pain. Here are some tips if you're running into trouble
* If Brew complains and tells you to run something like "sudo chown ....", do what it says
* If you're not seeing a cute panda following a square when running the demo, but some really ugly looking thing, you will have to downgrade SDL_image from 1.2.12 to 1.2.10. This is a bit involved, so let me know if you run into this problem

##Download PyGame with brew + pip (Mac)
Follow the instructions here:
http://pygame.org/wiki/macintosh

This should be a lot simpler than the Mac installation instructions above. If you already have _XQuartz_, _brew_, _pip3_, then you can just run the last couple steps without restarting:

(1) Install Python3 "proper" and packages we’ll need for installing PyGame from bitbucket:
brew install python3 hg sdl sdl_image sdl_mixer sdl_ttf portmidi

(2) Install PyGame:
pip3 install hg+http://bitbucket.org/pygame/pygame

##PortAudio
To test out the port audio, https://people.csail.mit.edu/hubert/pyaudio/


Run
```
python3 demo2.py
```
