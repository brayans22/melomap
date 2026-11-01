"""Tests unitarios de melomap_ingest.countries.

Convención: cada test prueba UNA cosa y su nombre dice cuál.
Estructura de cada test: Arrange (preparar) · Act (ejecutar) · Assert (comprobar).
"""

from __future__ import annotations

import dataclasses

import pytest

from melomap_ingest.countries import (
    CountriesConfigError,
    Country,
    Region,
    Source,
    group_by_region,
    load_countries,
)

VALID_YAML = """
countries:
  - code: MX
    name_es: México
    name_en: Mexico
    region: la
    sources: [apple, lastfm]
  - code: ES
    name_es: España
    name_en: Spain
    region: eu
    sources: [apple]
  - code: AR
    name_es: Argentina
    name_en: Argentina
    region: la
    sources: [lastfm]
"""


# --- Caso feliz ---------------------------------------------------------------


def test_load_countries_reads_all_entries(write_yaml):
    # Arrange
    path = write_yaml(VALID_YAML)
    # Act
    countries = load_countries(path)
    # Assert
    assert [c.code for c in countries] == ["MX", "ES", "AR"]


def test_load_countries_converts_types(write_yaml):
    mexico = load_countries(write_yaml(VALID_YAML))[0]
    assert mexico.region is Region.LATIN_AMERICA
    assert mexico.sources == (Source.APPLE, Source.LASTFM)


def test_country_name_by_language(write_yaml):
    mexico = load_countries(write_yaml(VALID_YAML))[0]
    assert mexico.name() == "México"
    assert mexico.name("en") == "Mexico"


def test_country_is_immutable(write_yaml):
    mexico = load_countries(write_yaml(VALID_YAML))[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        mexico.code = "XX"  # type: ignore[misc]


def test_group_by_region_keeps_order(write_yaml):
    groups = group_by_region(load_countries(write_yaml(VALID_YAML)))
    assert [c.code for c in groups[Region.LATIN_AMERICA]] == ["MX", "AR"]
    assert [c.code for c in groups[Region.EUROPE]] == ["ES"]


def test_real_config_file_is_valid(real_countries_file):
    """El archivo real del proyecto debe cargar sin errores y tener 31 países."""
    countries = load_countries(real_countries_file)
    assert len(countries) == 31
    assert all(isinstance(c, Country) for c in countries)


# --- Errores ------------------------------------------------------------------
# parametrize ejecuta el MISMO test con varios datos distintos.


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("countries: [", "no es un YAML válido"),
        ("paises: []", "debe tener una lista bajo la clave 'countries'"),
        ("countries:\n  - code: MX\n", "faltan los campos"),
        (
            "countries:\n  - {code: mex, name_es: a, name_en: a, region: la, sources: [apple]}",
            "código inválido",
        ),
        (
            "countries:\n  - {code: MX, name_es: a, name_en: a, region: xx, sources: [apple]}",
            "región desconocida",
        ),
        (
            "countries:\n  - {code: MX, name_es: a, name_en: a, region: la, sources: []}",
            "al menos una fuente",
        ),
        (
            "countries:\n  - {code: MX, name_es: a, name_en: a, region: la, sources: [spotify]}",
            "fuente desconocida",
        ),
        (
            "countries:\n"
            "  - {code: MX, name_es: a, name_en: a, region: la, sources: [apple]}\n"
            "  - {code: MX, name_es: b, name_en: b, region: la, sources: [apple]}",
            "repetido",
        ),
    ],
)
def test_invalid_config_raises_clear_error(write_yaml, content, message):
    with pytest.raises(CountriesConfigError, match=message):
        load_countries(write_yaml(content))


def test_missing_file_raises(tmp_path):
    with pytest.raises(CountriesConfigError, match="No existe"):
        load_countries(tmp_path / "no-existe.yaml")
