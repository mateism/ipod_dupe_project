from pathlib import Path
from typing import List

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class Track:
    def __init__(self, path: Path, title: str, artist: str, album: str, duration: int, size: int):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # seconds
        self.size = size  # bytes

    def __str__(self) -> str:
        minutes = self.duration // 60
        seconds = self.duration % 60
        size_kb = self.size // 1024
        return f"{self.title} – {self.artist} ({minutes}:{seconds:02d}, {size_kb} KB)"


def scan_music(music_dir: Path) -> List[Track]:
    """
    Recursively scan `music_dir` for .mp3 files and return a list of Track objects.
    """
    if not music_dir.is_dir():
        raise ValueError(f"Music directory does not exist: {music_dir}")

    mp3_files = list(music_dir.rglob("*.mp3"))
    print(f"Found {len(mp3_files)} MP3 files:")

    tracks: List[Track] = []

    for path in mp3_files:
        try:
            audio = MP3(path, ID3=EasyID3)

            title = audio.get("title", [path.stem])[0]
            artist = audio.get("artist", ["Unknown Artist"])[0]
            album = audio.get("album", ["Unknown Album"])[0]

            duration = int(audio.info.length)

            size = path.stat().st_size

            track = Track(
                path=path,
                title=title,
                artist=artist,
                album=album,
                duration=duration,
                size=size
            )

            tracks.append(track)

        except Exception as e:
            print(f"Failed to read metadata for {path.name}: {e}")

    return tracks

music_dir = Path("music")

scan_music(music_dir)

def load_default_library() -> list[Track]:
    """
    Scan the default 'music/' directory and return a list of Track objects.
    """
    return scan_music(Path("music"))