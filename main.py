from pathlib import Path

import pygame

from audio import AudioPlayer
from library import scan_music


# UI constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FONT_SIZE = 18
VISIBLE_ROWS = 12  # how many tracks to show at once


def main() -> None:
    music_dir = Path("music")
    tracks = scan_music(music_dir)

    if not tracks:
        print("No MP3 files found in 'music/'")
        return

    # Initialize pygame display (UI owns the window)
    pygame.init()  # safe even though AudioPlayer will call pygame.init() too
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("iPod Dupe – Browser")
    font = pygame.font.SysFont(None, FONT_SIZE)

    # Initialize audio engine
    player = AudioPlayer()
    player.init()  # just audio; no window creation inside audio.py

    selected_index = 0
    top_index = 0  # index of first visible row

    def draw():
        screen.fill((0, 0, 0))  # black

        bottom_index = min(top_index + VISIBLE_ROWS, len(tracks))
        y = 10

        for i in range(top_index, bottom_index):
            track = tracks[i]
            # Short label to fit on screen
            playing_marker = "> " if (player.current_track == track.path and player.is_playing) else "  "
            text = playing_marker + f"{track.artist} – {track.title}"

            if i == selected_index:
                # Highlight bar
                bg_color = (191, 148, 228)      # bright lavender
                fg_color = (0, 0, 0)            # black text
                pygame.draw.rect(
                    screen,
                    bg_color,
                    pygame.Rect(5, y - 2, SCREEN_WIDTH - 10, FONT_SIZE + 4),
                )
            else:
                fg_color = (255, 255, 255)      # white text

            text_surf = font.render(text[:60], True, fg_color)
            screen.blit(text_surf, (10, y))
            y += FONT_SIZE + 6

        # Optional: bottom status line (playing/paused)
        status_text = "PLAYING" if player.is_playing else "PAUSED"
        status_surf = font.render(status_text, True, (200, 200, 200))
        screen.blit(status_surf, (10, SCREEN_HEIGHT - FONT_SIZE - 10))

        pygame.display.flip()

    # Start by playing the first track
    print("\nStarting with:")
    print(tracks[0])
    player.play(tracks[0].path)

    running = True
    draw()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed → exiting")
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if selected_index < len(tracks) - 1:
                        selected_index += 1
                        # scroll window if needed
                        if selected_index >= top_index + VISIBLE_ROWS:
                            top_index += 1
                        draw()

                elif event.key == pygame.K_UP:
                    if selected_index > 0:
                        selected_index -= 1
                        if selected_index < top_index:
                            top_index = max(0, top_index - 1)
                        draw()

                elif event.key == pygame.K_RETURN:
                    # Enter → play selected track
                    track = tracks[selected_index]
                    print(f"Playing: {track}")
                    player.play(track.path)
                    draw()

                elif event.key == pygame.K_SPACE:
                    player.toggle_pause()
                    draw()

                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    print("Quit key pressed → exiting")
                    running = False

        # No continuous redraw for now; only on input.

    player.stop()


if __name__ == "__main__":
    main()