"""Carga y validación de la lista de países de MeloMap.

Este módulo es el primer código real del proyecto y está pensado para aprender:

* Type hints en cada función, clase y variable importante.
* ``dataclass`` inmutables (``frozen=True``) para representar datos.
* ``StrEnum`` para valores cerrados (regiones y fuentes).
* Errores propios con mensajes claros.
* ``pathlib.Path`` en vez de rutas como texto.

La configuración vive en ``config/countries.yaml`` y no en el código: así se
puede agregar un país sin tocar Python.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml

# Un código de país ISO 3166-1 alfa-2: exactamente dos letras mayúsculas.
_COUNTRY_CODE = re.compile(r"^[A-Z]{2}$")


class Region(StrEnum):
    """Regiones musicales en las que MeloMap agrupa los países."""

    NORTH_AMERICA = "na"
    LATIN_AMERICA = "la"
    EUROPE = "eu"
    MIDDLE_EAST = "me"
    AFRICA = "af"
    SOUTH_ASIA = "as"
    EAST_ASIA = "kp"
    OCEANIA = "oc"


class Source(StrEnum):
    """Fuentes de datos externas que se consultan para cada país."""

    APPLE = "apple"
    LASTFM = "lastfm"


class CountriesConfigError(ValueError):
    """El archivo de países no existe, no es YAML válido o tiene datos incorrectos."""


@dataclass(frozen=True, slots=True)
class Country:
    """Un país de MeloMap.

    ``frozen=True`` hace el objeto inmutable (no se puede modificar después de
    crearlo) y ``slots=True`` lo hace más liviano en memoria.
    """

    code: str
    name_es: str
    name_en: str
    region: Region
    sources: tuple[Source, ...]

    def name(self, lang: str = "es") -> str:
        """Devuelve el nombre del país en el idioma pedido (``es`` o ``en``)."""
        return self.name_en if lang == "en" else self.name_es


def parse_country(raw: Mapping[str, Any], index: int) -> Country:
    """Convierte un elemento crudo del YAML en un ``Country`` validado.

    Args:
        raw: Diccionario leído del YAML.
        index: Posición en la lista (para mensajes de error útiles).

    Raises:
        CountriesConfigError: Si falta un campo o algún valor no es válido.
    """
    where = f"país #{index + 1}"
    required = ("code", "name_es", "name_en", "region", "sources")
    missing = [field for field in required if field not in raw]
    if missing:
        raise CountriesConfigError(f"{where}: faltan los campos {', '.join(missing)}")

    code = str(raw["code"])
    if not _COUNTRY_CODE.match(code):
        raise CountriesConfigError(f"{where}: código inválido {code!r} (usa dos letras, ej. MX)")

    try:
        region = Region(raw["region"])
    except ValueError as exc:
        valid = ", ".join(r.value for r in Region)
        raise CountriesConfigError(
            f"{code}: región desconocida {raw['region']!r} (válidas: {valid})"
        ) from exc

    raw_sources = raw["sources"]
    if not isinstance(raw_sources, list) or not raw_sources:
        raise CountriesConfigError(f"{code}: 'sources' debe ser una lista con al menos una fuente")
    try:
        sources = tuple(Source(s) for s in raw_sources)
    except ValueError as exc:
        valid = ", ".join(s.value for s in Source)
        raise CountriesConfigError(f"{code}: fuente desconocida (válidas: {valid})") from exc

    return Country(
        code=code,
        name_es=str(raw["name_es"]),
        name_en=str(raw["name_en"]),
        region=region,
        sources=sources,
    )


def load_countries(path: Path) -> list[Country]:
    """Lee ``countries.yaml`` y devuelve la lista de países validada.

    Raises:
        CountriesConfigError: Si el archivo no existe, no es YAML válido,
            no tiene la clave ``countries`` o hay códigos repetidos.
    """
    if not path.is_file():
        raise CountriesConfigError(f"No existe el archivo {path}")

    try:
        # safe_load nunca ejecuta código: es la forma segura de leer YAML.
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CountriesConfigError(f"{path} no es un YAML válido: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("countries"), list):
        raise CountriesConfigError(f"{path} debe tener una lista bajo la clave 'countries'")

    countries = [parse_country(item, i) for i, item in enumerate(data["countries"])]

    seen: set[str] = set()
    for country in countries:
        if country.code in seen:
            raise CountriesConfigError(f"Código de país repetido: {country.code}")
        seen.add(country.code)

    return countries


def group_by_region(countries: Iterable[Country]) -> dict[Region, list[Country]]:
    """Agrupa los países por región, conservando el orden original."""
    groups: dict[Region, list[Country]] = {}
    for country in countries:
        groups.setdefault(country.region, []).append(country)
    return groups
