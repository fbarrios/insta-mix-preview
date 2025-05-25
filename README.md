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

Random squares of the album cover passed will be used as a background.

Output is in the output directory.

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

