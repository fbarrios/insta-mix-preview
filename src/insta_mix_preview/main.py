from .visualize import create_visualization, FPS
from .constants import DEFAULT_LENGTH_S, OUTPUT_WIDTH, OUTPUT_HEIGHT

from PIL import Image

import subprocess
import os
import logging

SNIPPET_FILE_FORMAT       = "{base}-snippet-{i}.wav"
VISUALIZATION_FILE_FORMAT = "{base}-snippet-{i}-visualization.mp4"
OUTPUT_FILE_FORMAT        = "{base}-snippet-{i}.mp4"


def _extract_snippets(audio_file, start_times, duration, output_dir):
    filename, ext = os.path.splitext(os.path.basename(audio_file))
    for i, start in enumerate(start_times, 1):
        output_filename = SNIPPET_FILE_FORMAT.format(base=filename, i=i)
        output_path     = os.path.join(output_dir, output_filename)

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


def generate_snippets(audio_filename, img_filename, snippets_begin, output_dir=None, length=DEFAULT_LENGTH_S):
    target_dir = output_dir or os.getcwd()
    os.makedirs(target_dir, exist_ok=True)

    # audio snippets
    _extract_snippets(audio_filename, snippets_begin, length, target_dir)

    # album cover snippets (shuffled so each snippet gets a random cover)
    source_img = Image.open(img_filename).convert("RGB")

    # resize the image to expected resolution
    img_resized = source_img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), resample=Image.LANCZOS)

    filename, ext = os.path.splitext(os.path.basename(audio_filename))
    for i in range(1, len(snippets_begin) + 1):
        snippet_filepath     = os.path.join(target_dir, SNIPPET_FILE_FORMAT.format(base=filename, i=i))
        visualization_output = os.path.join(target_dir, VISUALIZATION_FILE_FORMAT.format(base=filename, i=i))

        if os.path.exists(visualization_output):
            logging.info(f"{visualization_output} already exists, skipping visualization creation...")
        else:
            create_visualization(snippet_filepath, img_resized, visualization_output, length)

        output = os.path.join(target_dir, OUTPUT_FILE_FORMAT.format(base=filename, i=i))

        logging.info(f"Writing final output to {output}")
        # stich audio and video together
        # Instagram asks for the moov atom at the front of the file and no edit
        # lists: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
        # should construct a command such as:
        # ffmpeg -y \
        #     -i 251115_0185-snippet-2-visualization.mp4 \
        #     -i 251115_0185-snippet-2.wav \
        #     -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p \
        #     -bf 0 -g 30 -keyint_min 30 -sc_threshold 0 \
        #     -c:a aac -b:a 128k \
        #     -use_editlist 0 -movflags +faststart \
        #     251115_0185-snippet-2.mp4
        cmd = [
            "ffmpeg",
            "-v", "error",  # only shows erros for a cleaner output
            "-y",  # answers yes if file already exists

            "-i", visualization_output,
            "-i", snippet_filepath,

            "-c:v", "libx264",
            "-profile:v", "high",
            "-level", "4.1",
            "-pix_fmt", "yuv420p",
            "-bf", "0",  # no B-frames, they make the first timestamps negative
            "-g", str(FPS),  # one keyframe per second
            "-keyint_min", str(FPS),
            "-sc_threshold", "0",
            "-c:a", "aac",
            "-b:a", "128k",

            "-strict", "experimental",

            "-use_editlist", "0",
            "-movflags", "+faststart",  # moves the moov atom to the front

            output
        ]
        subprocess.run(cmd, check=True)

        # all went well, so now delete the files that we don't need anymore
        logging.info(f"Removing temp files")
        os.remove(visualization_output)
        os.remove(snippet_filepath)
