import argparse

from . import utils


def display_args(args) -> None:
    print("subsgen")
    print(f"  Path:       {args.path}")
    print(f"  Format:     {args.file_format or 'all supported'}")
    print(f"  Model:      {args.model}")
    print(f"  Language:   {args.language or 'auto-detect'}")
    print(f"  Translate:  {'yes' if args.translate else 'no'}")
    print(f"  Recursive:  {'yes' if args.recursive else 'no'}")
    print(f"  CPU:        {'yes' if args.cpu else 'no'}")
    print(f"  Save config:{'yes' if args.save_config else 'no'}")
    print(f"  Verbose:    {'yes' if args.verbose else 'no'}")


def parse_args() -> argparse.Namespace:
    from . import transcriber

    config = utils.load_config()
    parser = argparse.ArgumentParser(
        prog="subsgen",
        description="Auto-generate subtitles for video and audio files using Whisper AI.",
        epilog="Example: subsgen ./videos --model small --language es",
    )
    parser.set_defaults(**config)

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to a file or directory to process. Defaults to the current directory.",
    )

    parser.add_argument(
        "--file_format",
        default=None,
        help=(
            "Only process files with this extension. "
            "Accepts a single format or a comma-separated list (e.g. mp4 or mp4,mkv,mp3). "
            "Defaults to all supported video and audio formats."
        ),
    )

    parser.add_argument(
        "--model",
        default="base",
        metavar="LANG",
        choices=transcriber.SUPPORTED_MODELS,
        help=(
            "Whisper model to use for transcription. Larger models are more accurate but slower. "
            "English-only models (e.g. base.en) are faster for English content. "
            "Distilled models (e.g. distil-large-v3) offer a good speed/accuracy tradeoff. "
            "Defaults to 'base'."
        ),
    )

    parser.add_argument(
        "--language",
        metavar="LANG",
        default=None,
        choices=transcriber.SUPPORTED_LANGUAGES,
        help="Language code of the audio (e.g. en, es, fr). Defaults to auto-detection.",
    )

    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force CPU for transcription. Defaults to GPU (CUDA) if available.",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively search subdirectories for media files.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print detailed information about the files being processed.",
    )

    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate audio to English instead of transcribing in the original language.",
    )

    parser.add_argument(
        "--save-config",
        action="store_true",
        help="Save the current arguments to a config file for reuse.",
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available Whisper models and exit. See also: --model",
    )

    args = parser.parse_args()

    if args.list_models:
        utils.display_models()
        exit(0)

    if args.save_config:
        utils.save_config(args)

    if args.verbose:
        display_args(args)

    return args
