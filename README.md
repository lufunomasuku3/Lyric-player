Floating Lyrics Player

A Python desktop application that displays synchronised song lyrics in floating 
windows while audio plays.

The project uses Tkinter to create lyric cards and Pygame to play audio. 
Lyrics appear at specific timestamps, with typewriter text effect and an upward  floating animation.

Features
- Synchronised lyrics using audio playback time
- Floating lyrics cards that alternate between the left and right sides of the screen.
-Typewriter effect for displaying lyrics
- customisable lyrics timestamps
- Final lyrics moves towards the centre of the screen and stays visible until playback ends.
- Automatic application shutdown when the song finishes.

Technologies Used
- Python
- Tkinter
- Pygame CE
- Visual Studio Code

Requirements
-Python 3.14 or compatible  Python version
-Python CE
-Tkinter

Installation
1. Clone this repository: 
     git clone
     https://github.com/lufunomasuku3/Lyric-player.git

2. Open the project folder in VS Code.
3.Install Pygame CE:
python -m pi install pygame-ce

4.Add your own audio file to the project folder.
5. Make sure the audio filename matches the filename in  comeover.py
6. Run the application :  python comeover.py

Customising Lyrics
Lyrics and their starting timestamps are stored in the LYRICS list in  comeove.py.

Eg.
LYRICS = [
    (0.0, "First lyric"),
    (2.0, "Second lyric"),
    (5.0, "Third lyric"),
]

The timestamps are measured in seconds from the beginning of the audio.

Future Improvements
-Support for uploading audio files through the application
- Customisable lyric card colours and fonts
- Adjustable animation speed
- Support  for multiple songs and lyric files
- Improved lyric timing controls

Author
Created as personal Python programming project while learning desktop applications development.