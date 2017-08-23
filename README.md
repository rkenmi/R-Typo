# R-Typo
A Python game, homage to a classic arcade shoot-em-up using PyGame

<a href="https://youtu.be/_gXg7TGss5k">Demo Video</a>

Ripped R-Type sprites by Goemar from Retrogamezone.co.uk

# How to Run/Play

Visit the <a href="https://github.com/rkenmi/R-Typo/releases">releases</a> page to download the game.

For Windows users, simply double-click on **r-typo.exe** to launch the game and play.

For Ubuntu/Linux users, you can download the **r-typo** binary file and launch it with `./r-typo`

Alternatively, if your environment is setup correctly, you can launch the game via python using `python launcher.py`

# How to Build

The game is tested with the following:
- Python 3.5.1/3.4.3
- pygame 1.9.2a0/1.9.3
- PyTMX 3.20.14/3.21.3

An executable file can be built by using <a href="http://www.pyinstaller.org/">pyinstaller</a>:

First, install the requirements you need with `pip install -r requirements.txt`.

Then, install **pyinstaller** via pip and run the following commands:

On Windows:

    pyinstaller --add-data src;src --add-data sounds;sounds --add-data img;img --add-data sprites;sprites --add-data tilemap;tilemap --onefile launcher.py
    
On Linux/POSIX:

    pyinstaller --add-data src;src --add-data sounds;sounds --add-data img;img --add-data sprites;sprites --add-data tilemap;tilemap --onefile launcher.py

# Backstory

The game is set in the middle of 22nd century, and the player flies a futuristic fighter craft called the R-9a "Arrowhead", named for its shape, and because it is the ninth model in the 'R' series of fighter craft (but it is the first of the series to actually be used in combat; the previous models were all prototypes). 

The R-9a is warped into an alternate dimension called the NES. Unknown what the future holds, the player must control R-9a and move forward in hopes of returning back to its original dimension SNES.

# How to Play
W - The 'UP' movement key

A - The 'LEFT' movement key

S - The 'DOWN' movement key

D - The 'RIGHT' movement key


SPACEBAR - Shoot mini-missiles

E (Charge) - Shoots charged beams. The damage output and size of the beam depends on duration of charge.

RETURN/ENTER - Pauses the game. Also used to start the game at the launcher screen.
