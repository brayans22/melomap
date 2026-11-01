"""Comando de consola ``melomap-countries``.

Ejemplos (desde la raíz del repositorio, en PowerShell)::

    uv run melomap-countries
    uv run melomap-countries --lang en
    uv run melomap-countries --file config/countries.yaml

Separar la lógica (``countries.py``) de la interfaz de consola (este archivo)
permite probar cada parte por separado.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from melomap_ingest.countries import CountriesConfigError, group_by_region, load_countries

DEFAULT_FILE = Path("config/countries.yaml")


def build_parser() -> argparse.ArgumentParser:
    """Define los argumentos que acepta el comando."""
    parser = argparse.ArgumentParser(
        prog="melomap-countries",
        description="Muestra los países de MeloMap agrupados por región.",
    )
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="ruta a countries.yaml")
    parser.add_argument("--lang", choices=("es", "en"), default="es", help="idioma de los nombres")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada. Devuelve el código de salida: 0 si todo salió bien, 1 si hubo error."""
    args = build_parser().parse_args(argv)
    try:
        countries = load_countries(args.file)
    except CountriesConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for region, members in group_by_region(countries).items():
        names = ", ".join(c.name(args.lang) for c in members)
        print(f"[{region.value}] {names}")
    print(f"Total: {len(countries)} países")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
