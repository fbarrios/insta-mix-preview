from AudioAnalyzer import *
import random
import colorsys
import imageio.v3 as iio
import numpy as np
import pygame
import cv2
import math


filename = "bjork.wav"

analyzer = AudioAnalyzer()
analyzer.load(filename)

pygame.mixer.quit()
pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w / 2.2)
screen_h = int(infoObject.current_w / 2.2)

screen = pygame.Surface((screen_w, screen_h))

t = pygame.time.get_ticks()

timeCount = 0
avg_bass = 0
bass_trigger = -30
bass_trigger_started = 0

min_decibel = -80
max_decibel = 80

circle_color = (40, 40, 40)
polygon_default_color = [255, 255, 255]
polygon_bass_color = polygon_default_color.copy()
polygon_color_vel = [0, 0, 0]

poly = []
poly_color = polygon_default_color.copy()

circleX = int(screen_w / 2)
circleY = int(screen_h / 2)

min_radius = 100
max_radius = 150
radius = min_radius
radius_vel = 0

bass = {"start": 50, "stop": 100, "count": 12}
heavy_area = {"start": 120, "stop": 250, "count": 40}
low_mids = {"start": 251, "stop": 2000, "count": 50}
high_mids = {"start": 2001, "stop": 6000, "count": 20}

freq_groups = [bass, heavy_area, low_mids, high_mids]

bars = []
tmp_bars = []
length = 0

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


def rnd_color():
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

for group in freq_groups:
    g = []
    s = group["stop"] - group["start"]
    count = group["count"]
    reminder = s % count
    step = int(s / count)
    rng = group["start"]

    for i in range(count):
        if reminder > 0:
            reminder -= 1
            arr = np.arange(start=rng, stop=rng + step + 2)
            rng += step + 3
        else:
            arr = np.arange(start=rng, stop=rng + step + 1)
            rng += step + 2
        g.append(arr)
        length += 1

    tmp_bars.append(g)

angle_dt = 360 / length
ang = 0

for g in tmp_bars:
    gr = []
    for c in g:
        gr.append(
            RotatedAverageAudioBar(
                circleX + radius * math.cos(math.radians(ang - 90)),
                circleY + radius * math.sin(math.radians(ang - 90)),
                c, (255, 0, 255), angle=ang, width=8, max_height=370
            )
        )
        ang += angle_dt
    bars.append(gr)


# Frame capture list
screen = pygame.Surface((screen_w, screen_h))  # headless surface

running = True
duration_sec = 30
fps = 30
max_frames = int(duration_sec * fps)
frame_count = 0


# Setup OpenCV writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("output.mp4", fourcc, fps, (screen_w, screen_h))

frame_duration = 1 / fps
frame_count = 0
total_dur_secs = 10
max_frames = int(total_dur_secs * fps)



while running and frame_count < max_frames:
    avg_bass = 0
    poly = []

    t = pygame.time.get_ticks()

    time_sec = frame_count * frame_duration
    

    screen.fill(circle_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for b1 in bars:
        for b in b1:
            b.update_all(frame_duration, time_sec, analyzer)

    for b in bars[0]:
        avg_bass += b.avg

    avg_bass /= len(bars[0])

    if avg_bass > bass_trigger:
        if bass_trigger_started == 0:
            bass_trigger_started = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - bass_trigger_started) / 1000.0 > 2:
            polygon_bass_color = rnd_color()
            bass_trigger_started = 0
        if polygon_bass_color is None:
            polygon_bass_color = rnd_color()
        newr = min_radius + int(avg_bass * ((max_radius - min_radius) / (max_decibel - min_decibel)) + (max_radius - min_radius))
        radius_vel = (newr - radius) / 0.15
        polygon_color_vel = [(polygon_bass_color[x] - poly_color[x]) / 0.15 for x in range(len(poly_color))]
    elif radius > min_radius:
        bass_trigger_started = 0
        polygon_bass_color = None
        radius_vel = (min_radius - radius) / 0.15
        polygon_color_vel = [(polygon_default_color[x] - poly_color[x]) / 0.15 for x in range(len(poly_color))]
    else:
        bass_trigger_started = 0
        poly_color = polygon_default_color.copy()
        polygon_bass_color = None
        polygon_color_vel = [0, 0, 0]
        radius_vel = 0
        radius = min_radius

    radius += radius_vel * frame_duration

    for x in range(len(polygon_color_vel)):
        poly_color[x] = polygon_color_vel[x] * frame_duration + poly_color[x]

    for b1 in bars:
        for b in b1:
            b.x, b.y = circleX + radius * math.cos(math.radians(b.angle - 90)), circleY + radius * math.sin(math.radians(b.angle - 90))
            b.update_rect()
            poly.append(b.rect.points[3])
            poly.append(b.rect.points[2])

    draw_color = tuple(max(0, min(255, int(c))) for c in poly_color)
    # pygame.draw.polygon(screen, poly_color, poly)
    # pygame.draw.circle(screen, circle_color, (circleX, circleY), int(radius))

    draw_visualizer_frame(screen, analyzer, time_sec)

    frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    writer.write(frame_bgr)

    print(f"\rProcessing: {100 * frame_count // max_frames}%", end="", flush=True)
    frame_count += 1

writer.release()
print("\nDone.")
pygame.quit()

