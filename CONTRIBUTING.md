# Cómo trabajar en MeloMap

Estas reglas aplican aunque el proyecto lo hagas tú sola o solo: son las mismas que usan los equipos profesionales, y practicarlas es parte del aprendizaje.

## Flujo de trabajo

1. Actualiza `main`: `git switch main` y `git pull`.
2. Crea una rama por tarea: `git switch -c feat/carga-paises`.
3. Haz commits pequeños con mensajes de [Conventional Commits](#mensajes-de-commit).
4. Sube la rama: `git push -u origin feat/carga-paises`.
5. Abre un pull request y completa la plantilla.
6. Espera el CI en verde y revisa tu propio diff línea por línea.
7. Une con **Squash and merge** y borra la rama.

## Nombres de ramas

| Prefijo | Para qué |
| --- | --- |
| `feat/` | Funcionalidad nueva |
| `fix/` | Corrección de un error |
| `docs/` | Solo documentación |
| `test/` | Tests nuevos o mejorados |
| `refactor/` | Cambiar código sin cambiar lo que hace |
| `ci/` | Workflows de GitHub Actions |
| `chore/` | Mantenimiento (dependencias, configuración) |

## Mensajes de commit

Formato: `tipo(alcance opcional): descripción en minúsculas y en presente`

```text
feat(ingest): carga y valida la lista de países desde YAML
fix(ingest): rechaza códigos de país con minúsculas
test(ingest): cubre el caso de países repetidos
docs: agrega la guía de la fase 0
ci: ejecuta mypy en el workflow
```

Un cambio que rompe compatibilidad lleva `!`: `feat(api)!: cambia el formato de /countries`.

## Antes de abrir un pull request

```powershell
uv run ruff check .
uv run ruff format .
uv run mypy
uv run pytest
```

## Estilo de código

- Type hints en todas las funciones; `mypy --strict` sin errores.
- Funciones cortas, con un solo propósito y nombres que se explican solos.
- Docstrings en módulos, clases y funciones públicas.
- Cada error encontrado se convierte primero en un test que falla.
