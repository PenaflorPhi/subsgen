import pathlib
from typing import Optional

from tqdm import tqdm

from . import utils

SUPPORTED_LANGUAGES = utils.load_language_codes()
SUPPORTED_MODELS = {
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large-v1",
    "large-v2",
    "large-v3",
    "distil-small.en",
    "distil-medium.en",
    "distil-large-v2",
    "distil-large-v3",
}

HF_REPO = "Systran/faster-whisper-{model}"
CACHE_DIR = pathlib.Path.home() / ".cache" / "huggingface" / "hub"


def get_device(cpu: bool) -> tuple[str, str]:
    import torch

    if cpu:
        return "cpu", "int8"
    if torch.cuda.is_available():
        return "cuda", "float16"
    if torch.backends.mps.is_available():
        return "mps", "float16"
    return "cpu", "int8"


def is_model_cached(model: str) -> bool:
    repo_name = HF_REPO.format(model=model).replace("/", "--")
    return (CACHE_DIR / f"models--{repo_name}").exists()


def load_model(model: str, cpu: bool):
    from faster_whisper import WhisperModel

    utils.save_language_codes()

    device, compute_type = get_device(cpu)
    if not is_model_cached(model):
        print(
            f"Downloading model '{model}' for the first time, this may take a while..."
        )
    else:
        print(f"Loading model '{model}' on {device}...")
    return WhisperModel(model, device=device, compute_type=compute_type)


def transcribe(
    model,
    model_name: str,
    file: pathlib.Path,
    language: Optional[str],
    translate: bool = False,
    verbose: bool = False,
) -> tuple[list, str]:
    from faster_whisper import WhisperModel

    if verbose:
        print(f"\nTranscribing: {file.name}")

    try:
        active_model = model
        segments, info = active_model.transcribe(
            str(file),
            language=language,
            task="translate" if translate else "transcribe",
        )
    except RuntimeError as e:
        if "cuda" in str(e).lower() or "cublas" in str(e).lower():
            print("Warning: GPU failed during transcription, falling back to CPU...")
            active_model = WhisperModel(model_name, device="cpu", compute_type="int8")
            segments, info = active_model.transcribe(
                str(file),
                language=language,
                task="translate" if translate else "transcribe",
            )
        else:
            raise

    if verbose:
        print(
            f"Detected language: {info.language} (probability: {info.language_probability:.0%})"
        )

    segments_list = []
    with tqdm(
        total=round(info.duration, 2), unit="s", desc="Progress", disable=not verbose
    ) as pbar:
        for segment in segments:
            segments_list.append(segment)
            pbar.update(round(segment.end - pbar.n, 2))

    return segments_list, info.language
