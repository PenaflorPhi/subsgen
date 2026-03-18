import json
import pathlib
from typing import Any, Optional

CONFIG_DIR = pathlib.Path.home() / ".config" / "subsgen"
CONFIG_FILE = CONFIG_DIR / "config.json"


SUPPORTED_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mp3",
    ".wav",
    ".aac",
    ".ogg",
    ".flac",
    ".m4a",
    ".wma",
}


def resolve_files(
    path: str,
    file_format: Optional[str],
    recursive: bool = False,
    verbose: bool = False,
) -> list[pathlib.Path]:
    # Resolve path and validate it exists
    target = pathlib.Path(path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Path does not exist: {target}")

    # Get allowed extensions from file_format or fall back to SUPPORTED_EXTENSIONS
    if file_format:
        allowed = {f".{fmt.strip().lstrip('.')}" for fmt in file_format.split(",")}
    else:
        allowed = SUPPORTED_EXTENSIONS

    # Glob files recursively or shallowly depending on --recursive
    if target.is_file():
        files = [target]
    elif recursive:
        files = [f for f in target.rglob("*") if f.is_file()]
    else:
        files = [f for f in target.glob("*") if f.is_file()]

    # Return filtered list of files matching allowed extensions
    file_list = [f for f in files if f.suffix.lower() in allowed]

    if verbose:
        display_files(file_list)

    return file_list


def display_files(file_list: list[pathlib.Path]) -> None:
    print(f"\nFound {len(file_list)} file(s):")
    for file in file_list:
        print(f"  {file}")


def save_config(args) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = {
        "file_format": args.file_format,
        "model": args.model,
        "language": args.language,
        "translate": args.translate,
        "recursive": args.recursive,
        "cpu": args.cpu,
        "verbose": args.verbose,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Config saved to {CONFIG_FILE}")


def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def display_models() -> None:
    from . import transcriber

    print("Available models:\n")
    print("  Standard models:")
    standard = sorted(
        [m for m in transcriber.SUPPORTED_MODELS if not m.startswith("distil")]
    )
    for model in standard:
        print(f"    {model}")
    print("\n  Distilled models (faster, recommended):")
    distil = sorted([m for m in transcriber.SUPPORTED_MODELS if m.startswith("distil")])
    for model in distil:
        print(f"    {model}")
    print("\nTip: English-only models (e.g. base.en) are faster for English content.")
