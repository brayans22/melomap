"""Fixtures compartidas por todos los tests de melomap-ingest.

Una *fixture* es una función que prepara algo que los tests necesitan.
pytest la inyecta automáticamente en cualquier test que tenga un parámetro
con el mismo nombre.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def real_countries_file() -> Path:
    """Ruta al config/countries.yaml real del proyecto."""
    return REPO_ROOT / "config" / "countries.yaml"


@pytest.fixture
def write_yaml(tmp_path: Path) -> Callable[[str], Path]:
    """Devuelve una función que escribe un YAML temporal y retorna su ruta.

    ``tmp_path`` es una fixture incorporada de pytest: una carpeta temporal
    distinta para cada test, que se borra sola.
    """

    def _write(content: str) -> Path:
        path = tmp_path / "countries.yaml"
        path.write_text(content, encoding="utf-8")
        return path

    return _write
