
# Prof Tallman
# Simple music player using standard audio players that come with the OS.
#
# Program has a race condition that is obvious and simple to demonstrate. 
# The jukebox will play multiple audio files simultaneously. To exercise
# the bug, just issue the (P)lay command several times in quick succession.
# Students must fix this bug by adding appropriate wait logic.
#
# It is important to realize that this synchronization bug is simpler than
# most because people are familiar with music players. The idea of waiting
# for a song to finish comes naturally. Most race conditions can be fixed
# the same way by protecting access to a shared resource using a lock of
# some sort (e.g., mutexes, semaphores, critical sections, etc). The big
# difference is that identifying the data to protect is often more nuanced
# and the bugs are harder to detect.

from threading import Lock, Thread
from subprocess import Popen
from sys import platform
import os.path


class MediaPlayer:
    '''
    A class that plays WAV files using standard operating system tools.
    '''
    def __init__(self):
        '''
        Initializes the music player based on the host operating system.
        '''
        self._player_file = None
        self._player_args = None
        self._process = None
        self._lock = Lock()

        if platform == "win32":
            self._player_file = "powershell"
            self._player_args = "-c (New-Object Media.SoundPlayer '{}').PlaySync()"
        elif platform == "darwin":
            self._player_file = "afplay"
            self._player_args = "{}"
        elif platform == "linux":
            self._player_file = "play"
            self._player_args = "{}"
        else:
            raise ValueError("Unknown platform '{platform}'")
        return

    def __del__(self):
        '''
        Cleans up all resources belonging to the object.
        '''
        self.stop()
        return

    @property
    def is_busy(self):
        '''
        Returns whether a WAV file is currently playing.
        '''
        return self._lock.locked()

    def play(self, song):
        '''
        Starts playing the next song, if the player is available.
        '''
        if not os.path.isfile(song):
            raise ValueError(f"'{song}' is not a valid file")
        if self._lock.acquire(False):
            thread = Thread(target=self._play, args=(song,))
            thread.start()
            return
        
    def _play(self, song):
        '''
        Internal function that uses Popen to execute builtin media player.
        '''
        wav_file = self._player_args.format(song)
        cmd_line = [self._player_file, wav_file]  
        self._process = Popen(cmd_line, shell=False)
        self._process.wait()
        if self._lock.locked():
            self._process = None
            self._lock.release()

    def stop(self):
        if self._lock.locked():
            self._process.kill()
            self._process = None
            self._lock.release()
        return


def main():
    '''
    Runs the command-line based jukebox player
    '''

    # start the player with some preloaded songs (easier debugging)
    jukebox = MediaPlayer()
    playlist = [
        "BabyElephantWalk60.wav",
        "PinkPanther60.wav",
        "CantinaBand60.wav",
        "ImperialMarch60.wav",
        "StarWars60.wav",
    ]

    print("Welcome to Jukebox Player")
    print(" - (A)dd to playlist")
    print(" - (P)lay next song in playlist")
    print(" - (L)ist songs in the playlist")
    print(" - (S)kip current/next song")
    print(" - (Q)uit")
    print("--------------------------------")

    # Break the loop with 'Q' or 'X'
    while True:

        cmd = input("> ")
        if len(cmd) == 0:
            continue

        # Add a song to the playlist
        if cmd[0].upper() == "A":
            tokens = cmd.split(' ')
            if len(tokens) >= 2:
                song = tokens[1]
                playlist.append(song)

        # Play the next song in the queue
        elif cmd[0].upper() == "P":
            if not jukebox.is_busy and len(playlist) > 0:
                jukebox.play(playlist.pop(0))

        # List all of the songs in the queue
        elif cmd[0].upper() == "L":
            for i, song in enumerate(playlist):
                print(f"{i+1}: {song}")

        # Stop/skip the current song
        elif cmd[0].upper() == "S":
            if jukebox.is_busy:
                jukebox.stop()
            elif len(playlist) > 0:
                playlist.pop(0)

        # Quit or exit
        elif cmd[0].upper() == "Q" or cmd[0].upper() == 'X':
            jukebox.stop()
            break

        else:
            print(f"Invalid comment '{cmd[0]}'")
            continue

    return


if __name__ == "__main__":
    main()