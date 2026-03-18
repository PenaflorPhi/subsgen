from . import cli, subtitle, transcriber, utils


def main():
    args = cli.parse_args()

    file_list = utils.resolve_files(
        path=args.path,
        file_format=args.file_format,
        recursive=args.recursive,
        verbose=args.verbose,
    )

    if not file_list:
        print("No media files found.")
        return

    model = transcriber.load_model(args.model, args.cpu)

    for file in file_list:
        segments, language = transcriber.transcribe(
            model=model,
            model_name=args.model,
            file=file,
            language=args.language,
            translate=args.translate,
            verbose=args.verbose,
        )
        subtitle.write(file, segments)

    print(f"\nDone! Processed {len(file_list)} file(s).")


if __name__ == "__main__":
    main()
