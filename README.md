# Audio Visualizer

Visual representation of audio stream in terminal. Also provides helpful functions for
turning an audio stream into a representation that is friendly for graphical representation.
This is done by scaling the values in stream and interpolating them to create a stream
of frames for given fps, width and height.

```
usage: visualizer [-h] [-t TYPE] [-f FPS] [-w WIDTH] [-he HEIGHT] [-c CHAR]
                  [-d] [-ns]
                  filename

visualize audio

positional arguments:
  filename              path to audio file

options:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  file type of the audio file
  -f FPS, --fps FPS     frames per second for the graphical representation of
                        audio
  -w WIDTH, --width WIDTH
                        width of graphical representation of audio
  -he HEIGHT, --height HEIGHT
                        height of the graphical representation of audio
  -c CHAR, --char CHAR  char used to represent graph point
  -d, --debug           prints the number of skipped frames
  -ns, --nosync         do not sync graph with audio
```