from pathlib import Path
from typing import Optional

import pygame


class AudioPlayer:
    """
    Minimal pygame-based audio player for a single track at a time.
    Responsible ONLY for audio, not window/UI.
    """

    def __init__(self):
        self.is_initialized = False
        self.is_playing: bool = False
        self.current_track: Optional[Path] = None

    def init(self) -> None:
        if self.is_initialized:
            return

        # Configure audio BEFORE pygame.mixer.init
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()

        self.is_initialized = True
        print("Audio system initialized")

    def play(self, path: Path) -> None:
        if not self.is_initialized:
            self.init()

        print(f"Now playing: {path.name}")
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()

        self.current_track = path
        self.is_playing = True
        print("Initial state: PLAYING")

    def toggle_pause(self) -> None:
        if not self.is_initialized or self.current_track is None:
            return

        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("State change: PLAYING → PAUSED")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("State change: PAUSED → PLAYING")

    def stop(self) -> None:
        if not self.is_initialized:
            return

        print("Stopping playback and cleaning up")
        pygame.mixer.music.stop()
        pygame.quit()
        self.is_initialized = False
        self.is_playing = False
        self.current_track = None
        print("Exited cleanly")