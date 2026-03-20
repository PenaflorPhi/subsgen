from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    DANGER,
    EW,
    HORIZONTAL,
    LEFT,
    SECONDARY,
    SUCCESS,
    YES,
    E,
    W,
)

from . import main, transcriber, utils


def launch(args=None):
    root = ttk.Window(themename="darkly")
    root.geometry("780x560")
    root.minsize(640, 480)

    # --- State variables ---
    input_path = ttk.StringVar(value=args.path if args and args.path != "." else "")
    output_path = ttk.StringVar(value=args.output if args and args.output else "")
    file_format = ttk.StringVar(
        value=args.file_format if args and args.file_format else "All"
    )
    model = ttk.StringVar(value=args.model if args else "base")
    language = ttk.StringVar(
        value=args.language if args and args.language else "Auto detect"
    )
    flag_cpu = ttk.BooleanVar(value=args.cpu if args else False)
    flag_recursive = ttk.BooleanVar(value=args.recursive if args else False)
    flag_translate = ttk.BooleanVar(value=args.translate if args else False)
    flag_save_config = ttk.BooleanVar(value=args.save_config if args else False)

    # --- Directory pickers ---
    def pick_input():
        path = filedialog.askdirectory()
        if path:
            input_path.set(path)

    def pick_output():
        path = filedialog.askdirectory()
        if path:
            output_path.set(path)

    # --- Run ---
    def run():
        if not input_path.get():
            messagebox.showerror("Error", "Input directory is required.")
            return
        import argparse

        fmt = file_format.get()
        lang = language.get()
        args = argparse.Namespace(
            path=input_path.get(),
            output=output_path.get() or None,
            file_format=None if fmt == "All" else fmt,
            model=model.get(),
            language=None if lang == "Auto detect" else lang,
            cpu=flag_cpu.get(),
            recursive=flag_recursive.get(),
            translate=flag_translate.get(),
            save_config=flag_save_config.get(),
            verbose=False,
            list_models=False,
        )
        if args.save_config:
            utils.save_config(args)
        main.run(args)

    # --- Layout ---
    outer = ttk.Frame(root, padding=24)
    outer.pack(fill=BOTH, expand=YES)

    # Section: Directories
    ttk.Separator(outer, orient=HORIZONTAL).grid(
        row=1, column=0, columnspan=3, sticky=EW, pady=(0, 12)
    )
    ttk.Label(
        outer, text="DIRECTORIES", font=("", 9, "bold"), bootstyle=SECONDARY
    ).grid(row=2, column=0, columnspan=3, sticky=W, pady=(0, 8))

    ttk.Label(outer, text="Input directory").grid(row=3, column=0, sticky=W, pady=6)
    ttk.Entry(outer, textvariable=input_path).grid(row=3, column=1, padx=12, sticky=EW)
    ttk.Button(
        outer, text="Browse", command=pick_input, bootstyle=SECONDARY, width=10
    ).grid(row=3, column=2)

    ttk.Label(outer, text="Output directory").grid(row=4, column=0, sticky=W, pady=6)
    ttk.Entry(outer, textvariable=output_path).grid(row=4, column=1, padx=12, sticky=EW)
    ttk.Button(
        outer, text="Browse", command=pick_output, bootstyle=SECONDARY, width=10
    ).grid(row=4, column=2)

    # Section: Options
    ttk.Separator(outer, orient=HORIZONTAL).grid(
        row=5, column=0, columnspan=3, sticky=EW, pady=(16, 12)
    )
    ttk.Label(outer, text="OPTIONS", font=("", 9, "bold"), bootstyle=SECONDARY).grid(
        row=6, column=0, columnspan=3, sticky=W, pady=(0, 8)
    )

    ttk.Label(outer, text="File format").grid(row=7, column=0, sticky=W, pady=6)
    ttk.Combobox(
        outer,
        textvariable=file_format,
        values=["All"]
        + sorted([ext.lstrip(".") for ext in utils.SUPPORTED_EXTENSIONS]),
        state="readonly",
        width=28,
    ).grid(row=7, column=1, padx=12, sticky=W)

    ttk.Label(outer, text="Model").grid(row=8, column=0, sticky=W, pady=6)
    ttk.Combobox(
        outer,
        textvariable=model,
        values=sorted(list(transcriber.SUPPORTED_MODELS)),
        state="readonly",
        width=28,
    ).grid(row=8, column=1, padx=12, sticky=W)

    ttk.Label(outer, text="Language").grid(row=9, column=0, sticky=W, pady=6)
    ttk.Combobox(
        outer,
        textvariable=language,
        values=["Auto detect"] + sorted(list(transcriber.SUPPORTED_LANGUAGES)),
        state="readonly",
        width=28,
    ).grid(row=9, column=1, padx=12, sticky=W)

    # Section: Flags
    ttk.Separator(outer, orient=HORIZONTAL).grid(
        row=10, column=0, columnspan=3, sticky=EW, pady=(16, 12)
    )
    ttk.Label(outer, text="FLAGS", font=("", 9, "bold"), bootstyle=SECONDARY).grid(
        row=11, column=0, columnspan=3, sticky=W, pady=(0, 8)
    )

    flags_frame = ttk.Frame(outer)
    flags_frame.grid(row=12, column=0, columnspan=3, sticky=EW)

    ttk.Checkbutton(
        flags_frame, text="Force CPU", variable=flag_cpu, bootstyle="round-toggle"
    ).pack(side=LEFT, padx=(0, 24))
    ttk.Checkbutton(
        flags_frame, text="Recursive", variable=flag_recursive, bootstyle="round-toggle"
    ).pack(side=LEFT, padx=(0, 24))
    ttk.Checkbutton(
        flags_frame,
        text="Translate to English",
        variable=flag_translate,
        bootstyle="round-toggle",
    ).pack(side=LEFT, padx=(0, 24))
    ttk.Checkbutton(
        flags_frame,
        text="Save config",
        variable=flag_save_config,
        bootstyle="round-toggle",
    ).pack(side=LEFT)

    # Buttons
    ttk.Separator(outer, orient=HORIZONTAL).grid(
        row=13, column=0, columnspan=3, sticky=EW, pady=(20, 16)
    )
    btn_frame = ttk.Frame(outer)
    btn_frame.grid(row=14, column=0, columnspan=3, sticky=E)
    ttk.Button(
        btn_frame, text="Exit", command=root.destroy, bootstyle=DANGER, width=12
    ).pack(side=LEFT, padx=(0, 8))
    ttk.Button(btn_frame, text="Run", command=run, bootstyle=SUCCESS, width=12).pack(
        side=LEFT
    )

    outer.columnconfigure(1, weight=1)

    root.mainloop()
