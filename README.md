# Password Ninja Python Tools

Small Python tools for the Password Ninja API.

## What is included

- `password_ninja_cli.py` for command-line use
- `password_ninja_gui.py` for a Windows-friendly desktop app
- `password_ninja_api.py` as the shared API client

The tools target the v2 endpoint documented at `https://password.ninja/api`.

## Requirements

- Python 3.10 or newer
- No third-party packages are required for normal use

## Command Line

Generate one password:

```bash
python password_ninja_cli.py
```

Generate five passwords with capitals and 3 digits at the end:

```bash
python password_ninja_cli.py --num-of-passwords 5 --capitals --num-at-end 3
```

Print JSON output:

```bash
python password_ninja_cli.py --num-of-passwords 3 --json
```

## GUI

Launch the desktop app:

```bash
python password_ninja_gui.py
```

The GUI lets you adjust the API parameters, generate passwords, and copy the result to the clipboard.

## Build a Windows EXE

First create the Windows icon from the Password Ninja logo:

```bash
python build_password_ninja_icon.py
```

Then install PyInstaller and build the GUI app:

```bash
pip install pyinstaller
pyinstaller password_ninja_gui.spec
```

The executable will be created in `dist/` as `password-ninja-gui.exe`.

## Windows Launcher

If you just want a double-click launcher on Windows, run `launch_password_ninja_gui.bat`.
It expects Python to be installed and available on `PATH`.

## CI/CD Build

GitHub Actions can build the Windows EXE automatically from `.github/workflows/build-windows-exe.yml`.
The workflow uploads `dist/password-ninja-gui.exe` as a downloadable artifact on each push to `main` or `master`, and you can also run it manually from the Actions tab.

## GitHub Releases

Push a tag like `v1.0.0` to run `.github/workflows/release-desktop-packages.yml`.
That workflow builds installer-style desktop packages for Windows, macOS, and Linux, then attaches them to a GitHub Release.
You can also trigger it manually by supplying a tag in the Actions tab.

Release assets:

- `PasswordNinja.msi` for Windows
- `PasswordNinja-Portable-Windows.zip` for Windows portable use containing `PasswordNinjaPortable.exe`
- the portable app window will show `Password Ninja Portable`
- the portable build uses a distinct portable icon badge on Windows
- `PasswordNinja.dmg` for macOS
- `PasswordNinja.deb` for Linux
