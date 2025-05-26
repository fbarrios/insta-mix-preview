
from visualize import create_visualization
from crop import get_random_crops, get_bars_color

from PIL import Image

import subprocess
import os
import logging

OUTPUT_DIR = "output"

SNIPPET_FILE_FORMAT = "{base}-snippet-{i}.wav"
VISUALIZATION_FILE_FORMAT = "{base}-snippet-{i}-visualization.mp4"
OUTPUT_FILE_FORMAT = "{base}-snippet-{i}.mp4"

def _extract_snippets(audio_file, start_times, duration=10):
    filename, ext = os.path.splitext(audio_file)
    for i, start in enumerate(start_times, 1):
        output_filename = SNIPPET_FILE_FORMAT.format(base=filename, i=i)
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        if os.path.exists(output_path):
            logging.info(f"{output_path} already exists, skipping...")
            continue

        cmd = [
            "ffmpeg",
            "-v", "error",  # only shows erros for a cleaner output
            "-ss", str(start),
            "-t", str(duration),
            "-i", audio_file,
            "-c", "copy",  # avoid re-encoding
            output_path
        ]
        subprocess.run(cmd, check=True)


def create_preview(audio_filename, img_filename, snippets_begin):
    # audio snippets
    _extract_snippets(audio_filename, snippets_begin)

    # album cover snippets (shuffled so each snippet gets a random cover)
    source_img = Image.open(img_filename).convert("RGB")
    crops     = get_random_crops(source_img)
    ## bar_color = get_bars_color(source_img) this not used for now, will hardcode it white
    bar_color = (247, 247, 248)

    filename, ext = os.path.splitext(audio_filename)
    for i in range(1, len(snippets_begin) + 1):
        snippet_filepath = os.path.join(OUTPUT_DIR, SNIPPET_FILE_FORMAT.format(base=filename, i=i))
        visualization_output = os.path.join(OUTPUT_DIR, VISUALIZATION_FILE_FORMAT.format(base=filename, i=i))

        create_visualization(snippet_filepath, crops[i], bar_color, visualization_output)

        output = os.path.join(OUTPUT_DIR, OUTPUT_FILE_FORMAT.format(base=filename, i=i))
        # stich audio and video together
        # should construct a command such as:
        #   ffmpeg -y -i output.mp4 -i bjork.wav -c:v copy -c:a aac -strict experimental final_with_audio.mp4

        logging.info(f"Writing final output to {snippet_filepath}")
        cmd = [
            "ffmpeg",
            "-v", "error",  # only shows erros for a cleaner output
            "-y",  # answers yes if file already exists

            "-i", visualization_output,
            "-i", snippet_filepath,

            "-c:v", "copy",
            "-c:a", "aac",

            "-strict", "experimental",

            output
        ]
        subprocess.run(cmd, check=True)
