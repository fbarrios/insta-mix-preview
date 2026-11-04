import argparse
import logging
logging.basicConfig()

from .constants import DEFAULT_LENGTH_S
from .main import generate_snippets


def _to_wsl_path(path: str) -> str:
    """
    Convert Windows-style C: paths to their WSL equivalent.
    Keeps other paths unchanged so Linux paths keep working.
    """
    if path and path[1:2] == ':' and path[0].lower() == 'c':
        # strip the drive portion and normalize separators
        remainder = path.split(':', 1)[1].lstrip("\\/")  # remove leading slashes from remainder
        return "/mnt/c/" + remainder.replace("\\", "/")
    return path


def _parse_timestamp(ts: str) -> float:
    """Allow timestamps in seconds or mm:ss."""
    ts = ts.strip()
    if not ts:
        raise ValueError("empty timestamp")
    if ':' in ts:
        parts = ts.split(':')
        if len(parts) == 2:
            minutes, seconds = parts
            return float(minutes) * 60 + float(seconds)
        raise ValueError(f"unsupported timestamp format: {ts}")
    return float(ts)


def _positive_int(value: str) -> int:
    """argparse type for a whole number that is at least 1."""
    try:
        parsed = int(value)
    except ValueError:
        parsed = 0
    if parsed < 1:
        raise argparse.ArgumentTypeError(f"must be a whole number of seconds, at least 1: {value}")
    return parsed


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate square Instagram previews by overlaying audio snippets and a visualization on a cover image. Paths can be relative, absolute, or Windows-style (C:/...)."
    )
    parser.add_argument(
        '--cover',
        type=str,
        required=True,
        help='Path to the cover image (preferred PNG 1600x1600)'
    )
    parser.add_argument(
        '--audio',
        type=str,
        required=True,
        help='Path to the audio file to be processed (preferred WAV)'
    )
    parser.add_argument(
        '--snippets_start',
        type=str,
        default='',
        help='Comma-separated list of up to 5 timestamps in seconds or mm:ss for snippet start points'
    )
    parser.add_argument(
        '--length',
        type=_positive_int,
        default=DEFAULT_LENGTH_S,
        help='Length of each snippet in whole seconds (default: %(default)s)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='',
        help='Output directory, created if missing (default: the current directory)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    return parser.parse_args()

def main():
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(f"[DEBUG] Parsed arguments: {args}")
    else:
        logging.getLogger().setLevel(logging.INFO)

    cover_path = _to_wsl_path(args.cover)
    audio_path = _to_wsl_path(args.audio)
    output_dir = _to_wsl_path(args.output) if args.output else None
    if cover_path != args.cover or audio_path != args.audio or (args.output and output_dir != args.output):
        logging.debug(f"[DEBUG] Converted Windows-style paths -> cover: {cover_path}, audio: {audio_path}, output: {output_dir or '[default]'}")
    snippets = []
    if args.snippets_start:
        raw_snippets = [ts for ts in args.snippets_start.split(',') if ts.strip()]
        try:
            snippets = [_parse_timestamp(ts) for ts in raw_snippets]
        except ValueError as exc:
            logging.error(f"Invalid --snippets_start value: {exc}")
            raise SystemExit(2)

    logging.debug(f"[DEBUG] Cover path: {cover_path}")
    logging.debug(f"[DEBUG] Audio path: {audio_path}")
    logging.debug(f"[DEBUG] Output dir: {output_dir or '[default]'}")
    logging.debug(f"[DEBUG] Snippet start times: {snippets}")
    logging.debug(f"[DEBUG] Snippet length: {args.length}s")

    generate_snippets(audio_path, cover_path, snippets, output_dir, args.length)
