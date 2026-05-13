"""Download the Password Ninja logo and package it as a Windows ICO.

This avoids a third-party image dependency while still letting the GUI and
PyInstaller build use the brand logo as their icon.
"""

from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen
import struct
import ssl

try:
    import certifi
except ImportError:  # pragma: no cover - optional dependency
    certifi = None


LOGO_URL = "https://password.ninja/img/logo.png"
OUTPUT_DIR = Path("assets")
OUTPUT_FILE = OUTPUT_DIR / "password_ninja.ico"


def _read_png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Downloaded file is not a PNG image")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def _build_ico_from_png(png_data: bytes, width: int, height: int) -> bytes:
    image_count = 1
    icon_dir = struct.pack("<HHH", 0, 1, image_count)
    w = width if width < 256 else 0
    h = height if height < 256 else 0
    directory_entry = struct.pack(
        "<BBBBHHII",
        w,
        h,
        0,
        0,
        1,
        32,
        len(png_data),
        6 + 16,
    )
    return icon_dir + directory_entry + png_data


def main() -> int:
    OUTPUT_DIR.mkdir(exist_ok=True)
    context = ssl.create_default_context(cafile=certifi.where()) if certifi is not None else ssl.create_default_context()
    req = Request(LOGO_URL, headers={"User-Agent": "Mozilla/5.0 (PasswordNinjaIconBuilder/1.0)"})
    with urlopen(req, timeout=30, context=context) as response:
        png_data = response.read()

    width, height = _read_png_dimensions(png_data)
    ico_data = _build_ico_from_png(png_data, width, height)
    OUTPUT_FILE.write_bytes(ico_data)
    print(f"Wrote {OUTPUT_FILE} from {LOGO_URL} ({width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
