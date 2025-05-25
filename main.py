
from visualize import create_visualization

import subprocess
import os

OUTPUT_DIR = "output"

SNIPPET_FILE_FORMAT = "{base}-snippet-{i}.wav"
VISUALIZATION_FILE_FORMAT = "{base}-snippet-{i}-visualization.mp4"
OUTPUT_FILE_FORMAT = "{base}-snippet-{i}.mp4"

def extract_snippets(audio_file, start_times, duration=10):
    filename, ext = os.path.splitext(audio_file)
    for i, start in enumerate(start_times, 1):
        output_filename = SNIPPET_FILE_FORMAT.format(base=filename, i=i)
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        if os.path.exists(output_path):
            print(f"{output_path} already exists, skipping...")
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


input_filename = "bjork.wav"
snippets_begin = [30, 60, 120]
extract_snippets(input_filename, snippets_begin)

filename, ext = os.path.splitext(input_filename)

for i in range(1, len(snippets_begin) + 1):
    snippet_input = SNIPPET_FILE_FORMAT.format(base=filename, i=i)
    snippet_filepath = os.path.join(OUTPUT_DIR, snippet_input)
    visualization_output = VISUALIZATION_FILE_FORMAT.format(base=filename, i=i)
    visualization_path = os.path.join(OUTPUT_DIR, visualization_output)
    create_visualization(snippet_filepath, visualization_path)

    output = OUTPUT_FILE_FORMAT.format(base=filename, i=i)
    output_path = os.path.join(OUTPUT_DIR, output)
    # stich audio and video together
    #  ffmpeg -y -i output.mp4 -i bjork.wav -c:v copy -c:a aac -strict experimental final_with_audio.mp4
    cmd = [
        "ffmpeg",
        "-v", "error",  # only shows erros for a cleaner output
        "-y",  # answers yes if file already exists

        "-i", visualization_path,
        "-i", snippet_filepath,

        "-c:v", "copy",
        "-c:a", "aac",

        "-strict", "experimental",

        output_path
    ]
    subprocess.run(cmd, check=True)


