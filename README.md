TODO:
- push to github and make it available
- make logging better
    - stop showing pygame stuff
    - info by default all except errors or debug mode
- getopt
- instrucciones de instalación

# insta-mix-preview

This script receives as parameters the file paths of the mix cover (1600x1600
png file), the mix file (only tested with wav), and a list of the timestamps from
where 10s samples will be extracted.

It will generate up to 5 videos playing the samples in the background and a
visualization of the music with stacked bars. Videos will be in 1080x1080 which is
Instagram's suggested resolution (source: https://help.instagram.com/1631821640426723).

Random squares of the album cover passed will be used as a background. Output is in
the output directory.


Based originally on the project: https://gitlab.com/avirzayev/music-visualizer by
[Avi Rzayev](https://gitlab.com/avirzayev).

Sample song is [Coffee](https://freesound.org/people/tukyo.eth/sounds/608355/) by
tukyo.eth.

Sample cover is [white ceramic mug on brown wooden table](https://unsplash.com/photos/white-ceramic-mug-on-brown-wooden-table-S8daAB_nJSg)by Pariwat Pannium.

## Installation

1. Check which Python version you are running, this has been tested with 3.11.12

```
python --version
```

2. Create a new virtual environment and activate it

```
python3 -m venv venv
source venv/bin/activate
```

3. Install package requirements

```
pip install -r requirements.txt
```

4. Example test run:

```
python insta-mix-preview.py --cover="coffee.png" --audio="coffee.wav" --snippets_start=2,13,24
```

## Usage:

```bash
python insta-mix-preview.py --cover="path/to/cover.png" --audio="path/to/mix.wav" --snippets_start=20,90,210 [--debug] [--help]
```

Options:

- `--cover="file path"`: the cover that will be used as background (preferred: PNG 1600x1600)

- `--audio="file path"`: the audio file to be processed (preferred: WAV)

- `--snippets_start=...`: up to 5 comma-separated values of the timestamps where the snippets will start, in seconds

- `--debug`: print some extra debug information

- `--help`: this help

