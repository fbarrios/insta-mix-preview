# insta-mix-preview

This script receives as parameters the file paths of the mix cover (1600x1600
png file), the mix file (only tested with wav), and a list of the timestamps from
where 20s samples will be extracted.

It will generate up to 5 videos playing the samples in the background and a
visualization of the music with stacked bars. Videos will be in 1080x1080 which is
Instagram's suggested resolution (source: https://help.instagram.com/1631821640426723).

Output is in the "output" directory unless another path is passed with `--output`.

Based originally on the project: https://gitlab.com/avirzayev/music-visualizer by
[Avi Rzayev](https://gitlab.com/avirzayev).

Sample song is [Coffee](https://freesound.org/people/tukyo.eth/sounds/608355/) by
tukyo.eth.

Sample cover is [white ceramic mug on brown wooden table](https://unsplash.com/photos/white-ceramic-mug-on-brown-wooden-table-S8daAB_nJSg)by Pariwat Pannium.

## Installation

0. This requires ffmpeg installed (usually enough with `brew install ffmpeg`)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

That is the whole setup: uv fetches a suitable Python (3.11+) and the
dependencies on the first run, so there is no virtual environment to create or
activate.

2. Example test run:

```
uv run insta-mix-preview --cover="coffee.png" --audio="coffee.wav" --snippets_start=2,13,24
```

3. Optional — install it as a command available from anywhere, so it can be
   called without `uv run` and from outside this directory:

```
uv tool install .
insta-mix-preview --cover="coffee.png" --audio="coffee.wav" --snippets_start=2,13,24
```

## Usage:

```bash
uv run insta-mix-preview --cover="path/to/cover.png" --audio="path/to/mix.wav" --snippets_start=20,90,210 [--output="path/to/dir"] [--debug] [--help]
```

Options:

- `--cover="file path"`: the cover that will be used as background (preferred: PNG 1600x1600)

- `--audio="file path"`: the audio file to be processed (preferred: WAV)

- `--snippets_start=...`: up to 5 comma-separated values of the timestamps where the snippets will start, in seconds or `mm:ss`

- `--output="dir path"`: where to write the videos (default: the `output` directory)

- `--debug`: print some extra debug information

- `--help`: this help
