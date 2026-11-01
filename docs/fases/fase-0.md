# Fase 0 · Fundamentos: Git, Python moderno y estructura de proyecto

> **Duración:** 2 semanas a 10–12 horas por semana · **Sistema:** Windows 10/11 con PowerShell

## Qué vas a lograr

Al terminar esta fase tendrás en GitHub el repositorio de MeloMap con:

- Una estructura de carpetas profesional para todo el proyecto.
- Tu primer código en Python con **type hints** que lee y valida la lista de países desde un archivo **YAML**.
- **18 tests** con **100 % de cobertura** (el mínimo exigido es 90 %).
- Revisiones automáticas de estilo (**Ruff**), tipos (**mypy**) y secretos (**gitleaks**) antes de cada commit.
- Un pipeline de **CI en GitHub Actions** que corre todo en una máquina Windows en cada push.
- La rama `main` protegida: solo entra código por pull request y con el CI en verde.

Y lo más importante: vas a entender **por qué** existe cada archivo.

## Cómo usar esta guía

El zip trae el proyecto terminado. **No lo copies de golpe.** El método es:

1. Crea una carpeta vacía y ve construyendo el proyecto en el orden de esta guía.
2. Los archivos de configuración (`pyproject.toml`, `ci.yml`…) cópialos del zip **uno a uno**, leyendo la explicación de cada uno antes de pegarlo.
3. El código de Python (`countries.py`, `cli.py`) y los tests **escríbelos tú a mano**. Usa el zip solo para comparar cuando termines o si te atascas.
4. Haz cada ejercicio marcado con 🔧. Ahí es donde se aprende.

Cada parte termina con una pregunta de control. Si no la puedes responder sin mirar, repasa antes de seguir.

### Plan sugerido

| Sesión | Partes | Resultado |
| --- | --- | --- |
| 1 | 1 y 2 | Herramientas instaladas y PowerShell básico |
| 2 | 3 y 4 | Git configurado y primer commit en GitHub |
| 3 | 5 y 6 | Proyecto Python con uv y estructura de carpetas |
| 4 | 7 | YAML y `countries.yaml` |
| 5 | 8 | Type hints |
| 6 | 9 | `countries.py` escrito por ti |
| 7 | 10 | Tests y cobertura |
| 8 | 11, 12 y 13 | Ruff, pre-commit y el comando de consola |
| 9 | 14 y 15 | GitHub Actions y flujo con pull requests |
| 10 | 16 y 17 | Ejercicios de Git, documentación y cierre |

---

## Parte 1 · Instalar las herramientas

Abre **PowerShell** (menú Inicio → escribe “PowerShell”). Vamos a usar `winget`, el instalador oficial de paquetes de Windows.

```powershell
winget install --id Microsoft.PowerShell -e       # PowerShell 7, la versión moderna
winget install --id Git.Git -e                    # Git
winget install --id Microsoft.VisualStudioCode -e # editor
winget install --id astral-sh.uv -e               # gestor de Python y dependencias
winget install --id GitHub.cli -e                 # GitHub desde la terminal
```

Cierra la ventana y abre **PowerShell 7** (en el menú aparece como “PowerShell”, con icono negro). Comprueba:

```powershell
git --version
uv --version
gh --version
code --version
```

Instala Python 3.12 **a través de uv** (no desde python.org): así cada proyecto puede usar la versión exacta que necesita.

```powershell
uv python install 3.12
uv python list          # muestra las versiones disponibles e instaladas
```

En VS Code, cuando abras el proyecto, acepta instalar las extensiones recomendadas (las define `.vscode/extensions.json`).

> **Pregunta de control:** ¿por qué instalar Python con uv en vez de con el instalador de python.org?

---

## Parte 2 · PowerShell básico

PowerShell es la terminal y el lenguaje de automatización de Windows. Lo vas a usar en todas las fases, incluso para configurar los servidores.

| Para… | PowerShell | Alias corto |
| --- | --- | --- |
| Ver dónde estás | `Get-Location` | `pwd` |
| Moverte de carpeta | `Set-Location C:\proyectos` | `cd` |
| Listar archivos | `Get-ChildItem` | `ls`, `dir` |
| Crear carpeta | `New-Item -ItemType Directory nombre` | `mkdir` |
| Copiar | `Copy-Item origen destino` | `cp` |
| Borrar | `Remove-Item archivo` | `rm` |
| Ver un archivo | `Get-Content archivo` | `cat` |
| Variables de entorno | `$env:MELOMAP_ENV = "development"` | |
| Buscar un comando | `Get-Command *git*` | |
| Ayuda | `Get-Help Copy-Item -Examples` | |

PowerShell trabaja con **objetos**, no solo con texto. Por eso puedes encadenar comandos con `|` y filtrar por propiedades:

```powershell
Get-ChildItem -Recurse -Filter *.py | Select-Object Name, Length
```

🔧 **Ejercicio:** crea `C:\proyectos`, entra en ella y lista su contenido.

```powershell
mkdir C:\proyectos
cd C:\proyectos
ls
```

> **Pregunta de control:** ¿qué diferencia hay entre `cd` y `Set-Location`?

---

## Parte 3 · Git: conceptos y configuración

### Los cuatro lugares de Git

```text
 Carpeta de trabajo  ──git add──▶  Área de preparación  ──git commit──▶  Repositorio local  ──git push──▶  GitHub
   (tus archivos)                     (staging)                        (historial)                   (remoto)
```

- **Carpeta de trabajo:** los archivos como los ves en el editor.
- **Área de preparación (staging):** lo que elegiste incluir en el próximo commit.
- **Commit:** una foto con nombre de esos cambios. Tiene un identificador (hash), autor, fecha y mensaje.
- **Rama:** una línea de commits. `main` es la principal; cada tarea nueva va en su propia rama.
- **Remoto:** la copia en GitHub (`origin`).

### Configuración inicial (una sola vez por computadora)

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
git config --global init.defaultBranch main
git config --global core.autocrlf false     # los finales de línea los decide .gitattributes
git config --global pull.rebase true        # al hacer pull, reaplica tus commits encima
git config --global core.editor "code --wait"
git config --list --global                  # revisa lo que configuraste
```

Crea tu cuenta en [github.com](https://github.com) si no la tienes y conecta la terminal:

```powershell
gh auth login      # elige GitHub.com → HTTPS → Login with a web browser
```

> **Pregunta de control:** ¿qué diferencia hay entre `git add` y `git commit`?

---

## Parte 4 · Crear el repositorio

```powershell
cd C:\proyectos
mkdir melomap
cd melomap
git init
```

Crea el `.gitignore` y el `.gitattributes` **antes que nada**: así nunca se te escapa un secreto ni un problema de finales de línea. Cópialos del zip y lee sus comentarios.

- `.gitignore` le dice a Git qué no subir nunca: `.env`, `.venv`, cachés, datos, reportes.
- `.gitattributes` guarda los archivos con finales de línea LF (los de Linux y GitHub) aunque trabajes en Windows, salvo los scripts de PowerShell, que van con CRLF.

Crea un `README.md` mínimo y haz tu primer commit:

```powershell
"# MeloMap" | Out-File -Encoding utf8 README.md
git status                 # archivos nuevos en rojo: aún no están preparados
git add .gitignore .gitattributes README.md
git status                 # ahora en verde: preparados para el commit
git commit -m "chore: inicia el repositorio"
git log --oneline
```

Publica el repositorio en GitHub:

```powershell
gh repo create melomap --public --source . --push
```

Abre `https://github.com/TU-USUARIO/melomap` y verás tu commit.

> **Pregunta de control:** ¿por qué `.gitignore` va en el primer commit y no después?

---

## Parte 5 · Python moderno con uv

### Qué es uv y qué reemplaza

| Antes | Con uv |
| --- | --- |
| Instalador de python.org | `uv python install` |
| `python -m venv .venv` | Lo crea `uv sync` solo |
| `pip install` + `requirements.txt` | `uv add` + `pyproject.toml` |
| Versiones sin fijar | `uv.lock` con versiones exactas |
| Activar el entorno virtual | `uv run comando` lo usa directamente |

### El archivo `pyproject.toml`

Copia del zip el `pyproject.toml` de la raíz, `apps/ingest/pyproject.toml` y `.python-version`. Léelos con calma: cada sección tiene un comentario. Las ideas clave:

- **`[project]`** describe el proyecto: nombre, versión, Python requerido y dependencias.
- **`[tool.uv.workspace]`** convierte el repo en un **monorepo**: varias aplicaciones (hoy solo `apps/ingest`) que comparten un entorno y un lockfile.
- **`[dependency-groups] dev`** son herramientas para programar (pytest, mypy, Ruff) que **nunca** se instalan en producción.
- **`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.report]`** configuran todas las herramientas en un solo lugar.

### Instalar todo

```powershell
uv sync
```

Esto hace tres cosas: descarga Python 3.12 si falta, crea `.venv` y genera `uv.lock` con la versión exacta de cada dependencia. **El `uv.lock` sí se sube a Git**; `.venv` no.

Comandos que usarás a diario:

```powershell
uv add httpx                  # agrega una dependencia (no lo hagas aún: es de la fase 3)
uv add --dev pytest-mock      # agrega una herramienta de desarrollo
uv remove httpx               # la quita
uv run python --version       # ejecuta algo dentro del entorno del proyecto
uv lock --upgrade             # actualiza el lockfile a las últimas versiones permitidas
uv sync --locked              # instala exactamente lo del lockfile (lo usa el CI)
```

> **Pregunta de control:** ¿qué pasaría si no subes `uv.lock` y alguien instala el proyecto dentro de seis meses?

---

## Parte 6 · Estructura del proyecto

```text
melomap/
├─ .github/                  Automatización de GitHub (CI, Dependabot, plantillas)
├─ .vscode/extensions.json   Extensiones recomendadas para el editor
├─ apps/
│  ├─ ingest/                ← la app de esta fase
│  │  ├─ pyproject.toml
│  │  ├─ src/melomap_ingest/
│  │  │  ├─ __init__.py
│  │  │  ├─ countries.py     lógica: cargar y validar países
│  │  │  ├─ cli.py           interfaz de consola
│  │  │  └─ py.typed         marca el paquete como tipado
│  │  └─ tests/
│  │     ├─ conftest.py      fixtures compartidas
│  │     └─ unit/            tests unitarios
│  ├─ api/                   (fase 7)
│  └─ web/                   (fase 8)
├─ config/countries.yaml     configuración sin secretos
├─ db/ · warehouse/ · ml/ · infra/   (fases siguientes)
├─ docs/                     guías, ADR y diseño
├─ pyproject.toml · uv.lock · .python-version
├─ .gitignore · .gitattributes · .editorconfig · .env.example
├─ .pre-commit-config.yaml
└─ README.md · CHANGELOG.md · CONTRIBUTING.md · SECURITY.md · LICENSE
```

### Por qué el patrón `src/`

El código vive en `apps/ingest/src/melomap_ingest/` y no directamente en `apps/ingest/melomap_ingest/`. Así los tests importan **el paquete instalado**, no la carpeta por casualidad. Si algo no está bien empaquetado, el error aparece en tu computadora y no en el servidor.

### Por qué separar `countries.py` y `cli.py`

`countries.py` tiene la **lógica**; `cli.py` solo la **interfaz**. La lógica se puede reutilizar desde la API (fase 7) sin arrastrar nada de la consola, y cada parte se prueba por separado. Es el mismo principio que usarás en capas en la API.

🔧 **Ejercicio:** crea las carpetas a mano con PowerShell y copia los README de las carpetas futuras (`apps/api`, `apps/web`, `warehouse`, `ml`, `db`, `infra`). Git no guarda carpetas vacías: por eso cada una lleva un README que explica qué tendrá.

> **Pregunta de control:** ¿qué problema evita el patrón `src/`?

---

## Parte 7 · YAML

YAML es el formato de configuración que vas a usar en GitHub Actions, dbt, pre-commit, Dependabot, MkDocs y en la configuración de MeloMap.

### Sintaxis en cinco reglas

```yaml
# 1. Comentarios con almohadilla
nombre: MeloMap            # 2. clave: valor (un espacio después de los dos puntos)
version: 1                 #    número
activo: true               #    booleano
idiomas:                   # 3. lista: un guion por elemento
  - es
  - en
fuentes: [apple, lastfm]   #    lista en una línea
servidor:                  # 4. diccionario anidado: la sangría marca qué va dentro
  host: 10.10.0.20
  puerto: 5432
descripcion: |             # 5. texto de varias líneas
  Lo que suena en el mundo,
  ahora mismo.
```

**La sangría es con espacios, nunca con tabuladores**, y cambia el significado. Dos espacios por nivel es la convención.

### Errores típicos

| Error | Qué pasa | Solución |
| --- | --- | --- |
| Tabulador en la sangría | El archivo no carga | Configura el editor para usar espacios (`.editorconfig` ya lo hace) |
| `clave:valor` sin espacio | Se lee como un solo texto | Siempre `clave: valor` |
| `version: 1.10` | Se lee como el número 1.1 | Usa comillas: `"1.10"` |
| `code: NO` | Se lee como `false` (YAML 1.1) | Usa comillas: `"NO"` |

Ese último es famoso: el código de país de Noruega, `NO`, se convierte en `false`. PyYAML sigue YAML 1.1, así que te pasaría en MeloMap.

🔧 **Ejercicio:** copia `config/countries.yaml` del zip y lee el comentario del inicio. Después, en la Parte 10, agrega temporalmente Noruega **sin comillas** y mira qué error da tu validación. Luego ponle comillas y comprueba que funciona.

> **Pregunta de control:** ¿por qué la lista de países está en YAML y no escrita dentro del código Python?

---

## Parte 8 · Type hints

Python no obliga a declarar tipos, pero en un proyecto profesional se declaran siempre: documentan el código, mejoran el autocompletado y permiten que **mypy** encuentre errores antes de ejecutar.

### Lo básico

```python
nombre: str = "MeloMap"
paises: int = 31
bpm: float = 118.5
activo: bool = True

def saludo(nombre: str, veces: int = 1) -> str:
    return f"Hola {nombre}! " * veces
```

### Colecciones y valores opcionales

```python
codigos: list[str] = ["MX", "ES"]
posiciones: dict[str, int] = {"MX": 1, "ES": 3}
fuentes: tuple[str, ...] = ("apple", "lastfm")   # tupla de cualquier largo
vistos: set[str] = set()

def buscar(codigo: str) -> Country | None:       # puede devolver un país o None
    ...
```

### Tipos que vas a usar en MeloMap

```python
from collections.abc import Iterable, Mapping, Sequence, Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal

Idioma = Literal["es", "en"]          # solo acepta esos dos textos

class Region(StrEnum):                # valores cerrados con nombre
    EUROPE = "eu"

@dataclass(frozen=True, slots=True)   # clase de datos inmutable
class Country:
    code: str
    region: Region

def agrupar(paises: Iterable[Country]) -> dict[Region, list[Country]]:
    ...                               # Iterable: acepta lista, tupla o generador
```

**Regla práctica:** en los parámetros pide lo más general que te sirva (`Iterable`, `Mapping`); en el retorno devuelve lo más concreto (`list`, `dict`).

### mypy en modo estricto

`strict = true` en `pyproject.toml` exige tipos en todas las funciones y prohíbe atajos como `Any` implícito.

```powershell
uv run mypy
```

🔧 **Ejercicio:** cuando tengas `countries.py`, cambia el retorno de `load_countries` a `-> list[str]` y corre `uv run mypy`. Lee el error con calma: dice exactamente qué no coincide. Después déjalo como estaba.

> **Pregunta de control:** ¿qué diferencia hay entre recibir `list[Country]` y recibir `Iterable[Country]`?

---

## Parte 9 · Escribir `countries.py`

Escríbelo tú, en este orden. Después compáralo con el del zip.

1. **Los tipos de datos.** `Region` y `Source` como `StrEnum`, y `Country` como `dataclass(frozen=True, slots=True)` con `code`, `name_es`, `name_en`, `region` y `sources`. Agrega el método `name(lang)`.
2. **El error propio.** `class CountriesConfigError(ValueError)`. Tener tu propio tipo de error permite que quien llame a tu código capture solo tus errores.
3. **`parse_country(raw, index)`.** Convierte un diccionario del YAML en un `Country`. Valida en este orden: que estén todos los campos, que el código tenga dos letras mayúsculas, que la región exista y que las fuentes sean una lista válida. Cada error dice **qué país** falló y **por qué**.
4. **`load_countries(path)`.** Comprueba que el archivo existe, lo lee con `yaml.safe_load` (nunca `yaml.load`: `safe_load` no ejecuta código), valida la estructura, convierte cada país y rechaza códigos repetidos.
5. **`group_by_region(countries)`.** Devuelve un diccionario región → países.

Decisiones de diseño que vale la pena entender:

- **`frozen=True`:** un país no debería cambiar después de cargarse. Si algo intenta modificarlo, falla de inmediato.
- **`raise ... from exc`:** conserva el error original para depurar, pero muestra un mensaje claro.
- **`pathlib.Path`:** funciona igual en Windows y en cualquier sistema, sin pelear con `\` y `/`.
- **`encoding="utf-8"`:** obligatorio en Windows, donde la codificación por defecto puede no ser UTF-8 y romper la “é” de “México”.

Luego escribe `cli.py`: un `argparse` con `--file` y `--lang`, que imprime los países por región y devuelve `0` si todo salió bien o `1` si hubo error.

> **Pregunta de control:** ¿por qué `main()` devuelve un número en vez de imprimir y terminar?

---

## Parte 10 · Tests con pytest y coverage

### Anatomía de un test

```python
def test_load_countries_reads_all_entries(write_yaml):
    # Arrange: preparar los datos
    path = write_yaml(VALID_YAML)
    # Act: ejecutar lo que se prueba
    countries = load_countries(path)
    # Assert: comprobar el resultado
    assert [c.code for c in countries] == ["MX", "ES", "AR"]
```

### Herramientas de pytest que usa MeloMap

| Herramienta | Para qué | Dónde verla |
| --- | --- | --- |
| **Fixture** | Preparar algo reutilizable que pytest inyecta por nombre | `conftest.py` → `write_yaml` |
| **`tmp_path`** | Una carpeta temporal distinta para cada test | `conftest.py` |
| **`parametrize`** | El mismo test con muchos datos | `test_invalid_config_raises_clear_error` |
| **`pytest.raises`** | Comprobar que se lanza un error | Tests de errores |
| **`capsys`** | Capturar lo que se imprime | `test_cli.py` |

### Correr los tests

```powershell
uv run pytest                          # todos, con cobertura
uv run pytest -k cli                   # solo los que tienen "cli" en el nombre
uv run pytest -x                       # se detiene en el primer fallo
uv run pytest --cov-report=html        # reporte navegable
start htmlcov\index.html               # ábrelo en el navegador
```

### Cobertura: líneas y ramas

La cobertura mide qué parte del código se ejecutó durante los tests. MeloMap mide **ramas** (`--cov-branch`): no basta con pasar por un `if`, hay que probar el caso verdadero **y** el falso. El `pyproject.toml` exige un mínimo de 90 %: si baja, **los tests fallan**.

Cobertura alta no significa código sin errores. Significa que el código se ejecutó; si probaste los casos correctos depende de ti.

🔧 **Ejercicios:**

1. Comenta el caso `"repetido"` de la lista de `parametrize`, corre `uv run pytest` y mira qué línea queda sin cubrir en el reporte.
2. Agrega Noruega a `countries.yaml` **sin comillas** (`code: NO`), corre los tests y lee el error. Ponle comillas (`code: "NO"`) y comprueba que pasa. Luego quítala: el test exige 31 países.
3. Escribe un test nuevo: `group_by_region` con una lista vacía devuelve un diccionario vacío.

> **Pregunta de control:** ¿por qué 100 % de cobertura no garantiza que no haya errores?

---

## Parte 11 · Ruff: estilo y malas prácticas

Ruff reemplaza a varias herramientas antiguas (flake8, isort, black) y es muy rápido.

```powershell
uv run ruff check .          # busca problemas
uv run ruff check . --fix    # corrige los que puede solo
uv run ruff format .         # formatea todo el código
```

Las reglas activas están en `[tool.ruff.lint] select` del `pyproject.toml`, con un comentario por familia. Destacan `S` (seguridad, por ejemplo usar `yaml.load` en vez de `safe_load`), `ANN` (exige type hints) y `B` (errores comunes que parecen correctos).

🔧 **Ejercicio:** en `countries.py` cambia `yaml.safe_load` por `yaml.load` y corre `uv run ruff check .`. Lee qué regla salta y por qué es un riesgo de seguridad. Déjalo como estaba.

> **Pregunta de control:** ¿qué diferencia hay entre un linter y un formateador?

---

## Parte 12 · pre-commit y gitleaks

pre-commit ejecuta revisiones **antes** de que el commit exista. Si algo falla, el commit no se crea.

```powershell
uv run pre-commit install             # una vez por computadora
uv run pre-commit run --all-files     # pruébalo sobre todo el repo
```

La primera vez descarga las herramientas y tarda un poco. Revisa `.pre-commit-config.yaml`: valida YAML y TOML, limpia espacios, bloquea archivos enormes y marcas de conflicto, corre Ruff y busca secretos con gitleaks.

🔧 **Ejercicio:** crea `prueba.py` con una línea como `TOKEN = "ghp_"` seguida de 36 letras y números al azar (el formato de un token de GitHub). Intenta hacer commit: gitleaks lo bloqueará. Borra el archivo.

> **Pregunta de control:** si gitleaks está en pre-commit, ¿por qué también corre en el CI?

---

## Parte 13 · El comando de consola

`apps/ingest/pyproject.toml` declara un comando:

```toml
[project.scripts]
melomap-countries = "melomap_ingest.cli:main"
```

Después de `uv sync` lo puedes ejecutar:

```powershell
uv run melomap-countries
uv run melomap-countries --lang en
uv run melomap-countries --help
uv run melomap-countries --file no-existe.yaml ; $LASTEXITCODE   # devuelve 1
```

`$LASTEXITCODE` muestra el código de salida del último programa. Los servidores y el Programador de tareas de Windows usan ese número para saber si una tarea falló.

> **Pregunta de control:** ¿para qué sirve que el comando devuelva 0 o 1?

---

## Parte 14 · GitHub Actions: tu primer pipeline de CI

Copia `.github/workflows/ci.yml` del zip y léelo con sus comentarios. La estructura de todo workflow:

```yaml
name: CI                      # nombre que ves en GitHub
on:                           # CUÁNDO se ejecuta
  push:
    branches: [main]
  pull_request:
permissions:                  # qué puede hacer (mínimo privilegio)
  contents: read
jobs:                         # QUÉ trabajos hay
  quality:
    runs-on: windows-latest   # EN QUÉ máquina
    steps:                    # PASOS en orden
      - uses: actions/checkout@v4      # "uses" = una acción ya hecha
      - run: uv sync --locked          # "run" = un comando
```

Súbelo y míralo correr:

```powershell
git add .
git commit -m "ci: agrega el workflow de integración continua"
git push
gh run watch                  # sigue la ejecución desde la terminal
```

También lo ves en la pestaña **Actions** del repositorio. Haz clic en cada paso para leer sus logs.

🔧 **Ejercicio:** rompe un test a propósito, súbelo y lee en los logs de Actions por qué falló. Después arréglalo con un commit `fix: …`.

El badge del README (`ci.yml/badge.svg`) muestra en vivo si el CI está en verde. Reemplaza `TU-USUARIO` por tu usuario de GitHub.

> **Pregunta de control:** ¿por qué el CI usa `uv sync --locked` y no solo `uv sync`?

---

## Parte 15 · Trabajar como un equipo profesional

### Proteger `main`

En GitHub: **Settings → Rules → Rulesets → New branch ruleset**.

- Nombre: `proteger-main` · Enforcement: **Active** · Target: **Default branch**.
- Activa **Require a pull request before merging**.
- Activa **Require status checks to pass** y agrega `Calidad y tests`.
- Activa **Block force pushes**.

Desde ahora, nada entra a `main` sin pull request y CI en verde. Ni siquiera tú.

### El ciclo de cada tarea

```powershell
git switch main
git pull
git switch -c feat/test-grupo-vacio        # rama nueva
# ... escribe el código y los tests ...
git add .
git commit -m "test(ingest): cubre group_by_region con lista vacía"
git push -u origin feat/test-grupo-vacio
gh pr create --fill                       # abre el pull request
gh pr checks --watch                      # espera el CI
gh pr merge --squash --delete-branch      # une y borra la rama
```

Las convenciones de ramas y mensajes están en `CONTRIBUTING.md`.

### Activar Dependabot

**Settings → Code security** → activa **Dependabot alerts** y **Dependabot security updates**. El archivo `.github/dependabot.yml` ya pide revisiones semanales.

> **Pregunta de control:** ¿qué ganas haciendo pull requests si trabajas sola o solo?

---

## Parte 16 · Ejercicios de Git que tienes que dominar

### Ver el historial

```powershell
git log --oneline --graph --all
git show HEAD                 # el último commit en detalle
git diff                      # cambios sin preparar
git diff --staged             # cambios preparados
```

### Deshacer, de menor a mayor impacto

| Situación | Comando |
| --- | --- |
| Descartar cambios de un archivo sin commit | `git restore archivo` |
| Sacar un archivo del área de preparación | `git restore --staged archivo` |
| Corregir el mensaje del último commit (sin push) | `git commit --amend` |
| Deshacer el último commit pero conservar los cambios | `git reset --soft HEAD~1` |
| Deshacer un commit ya subido, sin reescribir historia | `git revert <hash>` |
| Guardar cambios a medias para cambiar de rama | `git stash` y luego `git stash pop` |

### 🔧 Provoca y resuelve un conflicto

```powershell
git switch -c rama-a
# edita la línea 1 de README.md: "# MeloMap · versión A"
git commit -am "docs: versión A del título"
git switch main
git switch -c rama-b
# edita la MISMA línea: "# MeloMap · versión B"
git commit -am "docs: versión B del título"
git merge rama-a              # ¡conflicto!
```

Git marca el archivo así:

```text
<<<<<<< HEAD
# MeloMap · versión B
=======
# MeloMap · versión A
>>>>>>> rama-a
```

Deja el texto final que quieras, borra las marcas y termina:

```powershell
git add README.md
git commit                    # Git propone un mensaje de merge
git log --oneline --graph
```

Al final, vuelve a `main` y borra las ramas de práctica: `git branch -D rama-a rama-b`.

### 🔧 Merge vs rebase

Repite el ejercicio, pero en vez de `git merge rama-a` usa `git rebase rama-a`. Compara los dos `git log --graph`: merge conserva la bifurcación con un commit de unión; rebase deja una línea recta. Regla: **nunca hagas rebase de una rama que otra persona ya descargó.**

---

## Parte 17 · Documentación

- **`README.md`:** la portada del proyecto y de tu portfolio. Debe decir qué es, mostrar una captura, explicar cómo ejecutarlo y cómo está hecho.
- **`CHANGELOG.md`:** qué cambió en cada versión, con versionado semántico (`MAYOR.MENOR.PARCHE`).
- **`CONTRIBUTING.md`:** las reglas del proyecto: ramas, commits y calidad.
- **`SECURITY.md`:** cómo reportar vulnerabilidades y qué prácticas sigue el proyecto.
- **`docs/adr/`:** las decisiones de arquitectura. Lee `0001-monorepo-con-uv.md`.
- **`docs/design/`:** el logo, la paleta y las pantallas aprobadas.
- **Docstrings:** el texto entre `"""` al inicio de cada módulo, clase y función.

🔧 **Ejercicio:** escribe `docs/adr/0002-type-hints-estrictos.md` usando la plantilla `0000-plantilla.md`: por qué el proyecto exige mypy en modo estricto, qué alternativas había y qué consecuencias tiene. Súbelo con un pull request.

---

## Cierre de la fase 0

### La dominas cuando…

- [ ] Resuelvo un conflicto de merge sin perder trabajo.
- [ ] Explico la diferencia entre merge y rebase y cuándo usar cada uno.
- [ ] Mi código pasa `mypy` en modo estricto.
- [ ] Cualquier persona clona el repo e instala todo con `uv sync`.

### Preguntas de entrevista

1. **¿Qué diferencia hay entre `git merge` y `git rebase`?** Merge une dos historias con un commit nuevo y conserva todo como pasó. Rebase reescribe tus commits encima de la otra rama y deja una historia lineal; no se usa en ramas compartidas.
2. **¿Para qué sirve un lockfile?** Para que todas las instalaciones usen exactamente las mismas versiones y se acabe el “en mi máquina funciona”.
3. **¿Por qué usar type hints si Python no los exige?** Documentan, mejoran el editor y permiten que mypy detecte errores antes de producción.
4. **¿Qué es CI?** Integración continua: cada cambio se prueba automáticamente (estilo, tipos, tests) antes de unirse a la rama principal.
5. **¿Cómo evitas subir un secreto a Git?** `.gitignore` para `.env`, `.env.example` sin valores, gitleaks en pre-commit y en el CI, y si se filtra uno, revocarlo de inmediato.

### Chuleta de comandos

```powershell
# Git
git status · git add . · git commit -m "tipo: mensaje" · git push
git switch -c rama · git switch main · git pull
git log --oneline --graph · git diff · git stash

# uv
uv sync · uv add paquete · uv add --dev paquete · uv run comando · uv lock --upgrade

# Calidad
uv run ruff check . --fix · uv run ruff format . · uv run mypy · uv run pytest
uv run pre-commit run --all-files

# GitHub CLI
gh repo create · gh pr create --fill · gh pr checks --watch · gh pr merge --squash --delete-branch · gh run watch
```

### Qué sigue

En la **fase 1** montas los servidores: tres máquinas virtuales con Windows Server en Hyper-V, la red interna entre ellas, el firewall y la VPN para administrarlas sin exponer nada a internet.
