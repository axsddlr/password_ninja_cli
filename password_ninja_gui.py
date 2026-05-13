"""Windows-friendly GUI for the Password Ninja API."""

from __future__ import annotations

import threading
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from password_ninja_api import DEFAULT_API_URL, PasswordNinjaError, PasswordNinjaOptions, generate_passwords


class PasswordNinjaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Password Ninja")
        self.geometry("820x620")
        self.minsize(760, 560)
        self._set_window_icon()

        self.base_url = tk.StringVar(value=DEFAULT_API_URL)
        self.min_pass_length = tk.StringVar(value="8")
        self.max_length = tk.StringVar(value="20")
        self.num_at_end = tk.StringVar(value="2")
        self.num_of_passwords = tk.StringVar(value="1")
        self.letters_for_numbers = tk.StringVar(value="0")
        self.letters_for_symbols = tk.StringVar(value="0")
        self.exclude_symbols = tk.StringVar(value="")

        self.animals = tk.BooleanVar(value=True)
        self.instruments = tk.BooleanVar(value=False)
        self.colours = tk.BooleanVar(value=False)
        self.shapes = tk.BooleanVar(value=False)
        self.food = tk.BooleanVar(value=False)
        self.sports = tk.BooleanVar(value=False)
        self.transport = tk.BooleanVar(value=False)
        self.symbols = tk.BooleanVar(value=False)
        self.capitals = tk.BooleanVar(value=False)
        self.spacers = tk.BooleanVar(value=False)
        self.rand_capitals = tk.BooleanVar(value=False)

        self.status = tk.StringVar(value="Ready")

        self._build_ui()

    def _set_window_icon(self) -> None:
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        icon_path = base_path.joinpath("assets", "password_ninja.ico")
        if icon_path.exists():
            try:
                self.iconbitmap(default=str(icon_path))
            except tk.TclError:
                pass

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Frame(self, padding=12)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="Password Ninja", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Generate kid-friendly passwords from the public API.").grid(row=1, column=0, sticky="w", pady=(4, 0))

        body = ttk.Frame(self, padding=(12, 0, 12, 12))
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)

        settings = ttk.LabelFrame(body, text="Settings", padding=12)
        settings.grid(row=0, column=0, columnspan=2, sticky="ew")
        settings.columnconfigure(1, weight=1)
        settings.columnconfigure(3, weight=1)

        self._add_labeled_entry(settings, 0, "API URL", self.base_url, width=58, columnspan=3)
        self._add_labeled_entry(settings, 1, "Min length", self.min_pass_length)
        self._add_labeled_entry(settings, 1, "Max length", self.max_length, column=2)
        self._add_labeled_entry(settings, 2, "Digits at end", self.num_at_end)
        self._add_labeled_entry(settings, 2, "Passwords", self.num_of_passwords, column=2)
        self._add_labeled_entry(settings, 3, "Letters -> numbers %", self.letters_for_numbers)
        self._add_labeled_entry(settings, 3, "Letters -> symbols %", self.letters_for_symbols, column=2)
        self._add_labeled_entry(settings, 4, "Exclude symbols", self.exclude_symbols, width=24, columnspan=3)

        options = ttk.LabelFrame(body, text="Word Lists and Effects", padding=12)
        options.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=(12, 0))
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)

        left_flags = [
            ("Animals", self.animals),
            ("Instruments", self.instruments),
            ("Colours", self.colours),
            ("Shapes", self.shapes),
            ("Food", self.food),
            ("Sports", self.sports),
            ("Transport", self.transport),
        ]
        right_flags = [
            ("Symbols", self.symbols),
            ("Capitals", self.capitals),
            ("Hyphen separators", self.spacers),
            ("Random capitals", self.rand_capitals),
        ]

        for index, (label, variable) in enumerate(left_flags):
            ttk.Checkbutton(options, text=label, variable=variable).grid(row=index, column=0, sticky="w", pady=2)
        for index, (label, variable) in enumerate(right_flags):
            ttk.Checkbutton(options, text=label, variable=variable).grid(row=index, column=1, sticky="w", pady=2)

        output = ttk.LabelFrame(body, text="Passwords", padding=12)
        output.grid(row=1, column=1, sticky="nsew", padx=(6, 0), pady=(12, 0))
        output.columnconfigure(0, weight=1)
        output.rowconfigure(1, weight=1)

        actions = ttk.Frame(output)
        actions.grid(row=0, column=0, sticky="ew")
        ttk.Button(actions, text="Generate", command=self.generate_passwords).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(actions, text="Copy All", command=self.copy_all).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(actions, text="Clear", command=self.clear_output).grid(row=0, column=2)

        self.text = tk.Text(output, height=18, wrap="none", font=("Consolas", 11))
        self.text.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        scrollbar = ttk.Scrollbar(output, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(10, 0))
        self.text.configure(yscrollcommand=scrollbar.set)

        statusbar = ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w", padding=(8, 4))
        statusbar.grid(row=2, column=0, sticky="ew")

    def _add_labeled_entry(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        variable: tk.StringVar,
        *,
        column: int = 0,
        columnspan: int = 1,
        width: int = 12,
    ) -> None:
        container = ttk.Frame(parent)
        container.grid(row=row, column=column, columnspan=columnspan, sticky="ew", pady=4, padx=4)
        container.columnconfigure(1, weight=1)
        ttk.Label(container, text=label).grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(container, textvariable=variable, width=width).grid(row=0, column=1, sticky="ew")

    def _read_options(self) -> PasswordNinjaOptions:
        return PasswordNinjaOptions(
            minPassLength=int(self.min_pass_length.get()),
            maxLength=int(self.max_length.get()),
            numAtEnd=int(self.num_at_end.get()),
            numOfPasswords=int(self.num_of_passwords.get()),
            animals=self.animals.get(),
            instruments=self.instruments.get(),
            colours=self.colours.get(),
            shapes=self.shapes.get(),
            food=self.food.get(),
            sports=self.sports.get(),
            transport=self.transport.get(),
            symbols=self.symbols.get(),
            capitals=self.capitals.get(),
            spacers=self.spacers.get(),
            randCapitals=self.rand_capitals.get(),
            lettersForNumbers=int(self.letters_for_numbers.get()),
            lettersForSymbols=int(self.letters_for_symbols.get()),
            excludeSymbols=self.exclude_symbols.get(),
        )

    def generate_passwords(self) -> None:
        self.status.set("Generating passwords...")
        self.text.delete("1.0", tk.END)

        try:
            options = self._read_options()
        except ValueError as exc:
            self._show_error(str(exc))
            return
        base_url = self.base_url.get()

        def worker() -> None:
            try:
                passwords = generate_passwords(options, base_url=base_url)
            except PasswordNinjaError as exc:
                self.after(0, lambda: self._show_error(str(exc)))
                return

            def finish() -> None:
                self.text.insert("1.0", "\n".join(passwords))
                self.status.set(f"Generated {len(passwords)} password(s).")

            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    def _show_error(self, message: str) -> None:
        self.status.set("Error")
        messagebox.showerror("Password Ninja", message)

    def copy_all(self) -> None:
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            self.status.set("Nothing to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        self.status.set("Passwords copied to clipboard.")

    def clear_output(self) -> None:
        self.text.delete("1.0", tk.END)
        self.status.set("Cleared.")


def main() -> None:
    app = PasswordNinjaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
