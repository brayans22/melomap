"""Tests del comando melomap-countries.

``capsys`` es una fixture de pytest que captura lo que se imprime en pantalla
(stdout y stderr) para poder comprobarlo.
"""

from __future__ import annotations

from melomap_ingest.cli import main


def test_cli_prints_countries_grouped(real_countries_file, capsys):
    exit_code = main(["--file", str(real_countries_file)])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "[la]" in out
    assert "México" in out
    assert "Total: 32 países" in out


def test_cli_english_names(real_countries_file, capsys):
    main(["--file", str(real_countries_file), "--lang", "en"])
    assert "Mexico" in capsys.readouterr().out


def test_cli_returns_1_on_error(tmp_path, capsys):
    exit_code = main(["--file", str(tmp_path / "no-existe.yaml")])
    assert exit_code == 1
    assert "Error:" in capsys.readouterr().err
