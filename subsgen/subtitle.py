import pathlib


def format_timestamp(seconds: float) -> str:
    # Convert seconds to SRT timestamp format HH:MM:SS,mmm
    milliseconds = int(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def format_segment(index: int, segment) -> str:
    # Format a single SRT block
    start = format_timestamp(segment.start)
    end = format_timestamp(segment.end)
    return f"{index}\n{start} --> {end}\n{segment.text.strip()}\n"


def write(file: pathlib.Path, segments: list) -> None:
    # Output file sits next to the source file with .srt extension
    output = file.with_suffix(".srt")

    with open(output, "w", encoding="utf-8") as f:
        for index, segment in enumerate(segments, start=1):
            f.write(format_segment(index, segment))
            f.write("\n")

    print(f"Saved: {output}")
