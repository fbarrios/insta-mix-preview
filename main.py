from AudioAnalyzer import AudioAnalyzer

import numpy as np
import pygame
import cv2

FPS = 30
FRAME_DURATION = 1 / FPS
FRAGMENT_DURATION_S = 10

NUMBER_OF_BARS = 50
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1350

BAR_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

BAR_AREA_TOP = SCREEN_HEIGHT * 2 // 3  # start of bottom third
BAR_AREA_BOTTOM = SCREEN_HEIGHT
BAR_AREA_HEIGHT = BAR_AREA_BOTTOM - BAR_AREA_TOP


def draw_visualizer_frame(screen, analyzer, time_sec):
    screen.fill(BACKGROUND_COLOR)

    fft = analyzer.fft(time_sec)
    band_size = len(fft) // NUMBER_OF_BARS
    bar_width = SCREEN_WIDTH // (NUMBER_OF_BARS + 1)

    for i in range(NUMBER_OF_BARS):
        start = i * band_size
        end = start + band_size
        amplitude = np.mean(fft[start:end])

        # Normalize amplitude
        amplitude = np.clip(amplitude, -80, 0)  # dBFS
        norm = (amplitude + 80) / 80  # 0.0 to 1.0

        # Scale to visual height
        bar_height = int(norm * BAR_AREA_HEIGHT)

        x = (i + 1) * bar_width
        y = BAR_AREA_BOTTOM - bar_height

        pygame.draw.rect(screen, BAR_COLOR, (x, y, bar_width // 2, bar_height))


def create_visualization(filename):
    analyzer = AudioAnalyzer()
    analyzer.load(filename)

    pygame.mixer.quit()
    pygame.init()

    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    # Setup OpenCV writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(f"{filename}-visualization.mp4", fourcc, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    frame_count = 0
    max_frames = int(FRAGMENT_DURATION_S * FPS)

    while running and frame_count < max_frames:
        time_sec = frame_count * FRAME_DURATION
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_visualizer_frame(screen, analyzer, time_sec)

        frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

        print(f"\rProcessing: {100 * frame_count // max_frames}%", end="", flush=True)
        frame_count += 1

    writer.release()
    pygame.quit()

    print("\nDone.")

create_visualization('bjork.wav')
