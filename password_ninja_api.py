"""Password Ninja API client helpers."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Iterable
from urllib import error, parse, request
import json
import ssl

try:
    import certifi
except ImportError:  # pragma: no cover - optional dependency
    certifi = None


DEFAULT_API_URL = "https://api.password.ninja/api/v2/password"


@dataclass(slots=True)
class PasswordNinjaOptions:
    minPassLength: int = 8
    maxLength: int = 20
    numAtEnd: int = 2
    numOfPasswords: int = 1
    animals: bool = True
    instruments: bool = False
    colours: bool = False
    shapes: bool = False
    food: bool = False
    sports: bool = False
    transport: bool = False
    symbols: bool = False
    capitals: bool = False
    spacers: bool = False
    randCapitals: bool = False
    lettersForNumbers: int = 0
    lettersForSymbols: int = 0
    excludeSymbols: str = ""


class PasswordNinjaError(RuntimeError):
    """Raised when the Password Ninja API request fails."""


def _iter_query_items(options: PasswordNinjaOptions) -> Iterable[tuple[str, str]]:
    for field in fields(options):
        value = getattr(options, field.name)
        if value is None:
            continue
        if isinstance(value, bool):
            if value:
                yield field.name, "true"
            continue
        if isinstance(value, str):
            if value:
                yield field.name, value
            continue
        yield field.name, str(value)


def build_url(options: PasswordNinjaOptions, base_url: str = DEFAULT_API_URL) -> str:
    query = parse.urlencode(list(_iter_query_items(options)))
    return f"{base_url}?{query}" if query else base_url


def _build_ssl_context() -> ssl.SSLContext:
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def generate_passwords(
    options: PasswordNinjaOptions,
    base_url: str = DEFAULT_API_URL,
    timeout: float = 30.0,
) -> list[str]:
    url = build_url(options, base_url=base_url)
    req = request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (PasswordNinjaPython/1.0)",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout, context=_build_ssl_context()) as response:
            payload = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else exc.reason
        raise PasswordNinjaError(f"API request failed ({exc.code}): {body}") from exc
    except error.URLError as exc:
        raise PasswordNinjaError(f"Could not reach Password Ninja: {exc.reason}") from exc

    try:
        data: Any = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise PasswordNinjaError("API returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise PasswordNinjaError("API returned an unexpected response.")

    if "error" in data:
        raise PasswordNinjaError(str(data["error"]))

    passwords = data.get("passwords")
    if not isinstance(passwords, list) or not all(isinstance(item, str) for item in passwords):
        raise PasswordNinjaError("API response did not include password strings.")

    return passwords
