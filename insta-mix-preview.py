import argparse
import logging
logging.basicConfig()

from main import create_preview


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a square Instagram preview by overlaying 10s audio snippets over a background cover."
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
        help='Comma-separated list of up to 5 timestamps in seconds for snippet start points'
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

    cover_path = args.cover
    audio_path = args.audio
    snippets = [float(ts) for ts in args.snippets_start.split(',') if ts.strip()] if args.snippets_start else []

    logging.debug(f"[DEBUG] Cover path: {cover_path}")
    logging.debug(f"[DEBUG] Audio path: {audio_path}")
    logging.debug(f"[DEBUG] Snippet start times: {snippets}")

    create_preview(audio_path, cover_path, snippets)

if __name__ == '__main__':
    main()
