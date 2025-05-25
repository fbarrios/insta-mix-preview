from AudioAnalyzer import AudioAnalyzer

import numpy as np
import pygame
import cv2

import os
os.environ["SDL_AUDIODRIVER"] = "dummy"


FPS = 30
FRAME_DURATION = 1 / FPS
FRAGMENT_DURATION_S = 10

NUMBER_OF_BARS = 50
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080

MARGIN_RATIO = 0.05
MARGIN_PX = int(SCREEN_HEIGHT * MARGIN_RATIO)

BAR_AREA_TOP = SCREEN_HEIGHT * 2 // 3 + MARGIN_PX
BAR_AREA_BOTTOM = SCREEN_HEIGHT - MARGIN_PX
BAR_AREA_HEIGHT = BAR_AREA_BOTTOM - BAR_AREA_TOP


def draw_visualizer_frame(screen, analyzer, bar_color, time_sec):
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

        pygame.draw.rect(screen, bar_color, (x, y, bar_width // 2, bar_height))


def background_pil_to_pygame(pil_img):
    arr = np.array(pil_img.convert("RGB"))
    surface = pygame.Surface((arr.shape[1], arr.shape[0]))
    pygame.surfarray.blit_array(surface, arr.swapaxes(0, 1))
    return surface


def create_visualization(input_filename, background_img, bar_color, output_filename):
    analyzer = AudioAnalyzer()
    analyzer.load(input_filename)

    pygame.mixer.quit()
    pygame.init()

    bg_surface = background_pil_to_pygame(background_img)
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Setup OpenCV writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_filename, fourcc, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    frame_count = 0
    max_frames = int(FRAGMENT_DURATION_S * FPS)

    running = True
    while running and frame_count < max_frames:
        time_sec = frame_count * FRAME_DURATION

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg_surface, (0, 0))
        draw_visualizer_frame(screen, analyzer, bar_color, time_sec)

        frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

        print(f"\rProcessing visualization for {output_filename}: {100 * frame_count // max_frames}% ", end="", flush=True)
        frame_count += 1

    writer.release()
    pygame.quit()

    print("Done.")

