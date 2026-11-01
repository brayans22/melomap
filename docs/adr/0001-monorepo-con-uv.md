# ADR 0001: monorepo con un workspace de uv

- **Estado:** aceptada
- **Fecha:** 2026-10-27

## Contexto

MeloMap tiene varias aplicaciones que comparten código y configuración: el ingestor, la API, el frontend, el warehouse y el modelo. Hace falta decidir si viven en un repositorio o en varios, y con qué herramienta se gestionan las dependencias de Python.

## Opciones consideradas

1. **Un repositorio por aplicación.** Aislamiento total, pero cambios que tocan varias partes requieren varios pull requests coordinados, y el CI y la configuración se duplican.
2. **Monorepo con pip + requirements.txt.** Simple de entender, pero sin lockfile real ni gestión de varios paquetes.
3. **Monorepo con Poetry.** Maduro, pero más lento y sin soporte nativo de workspaces.
4. **Monorepo con un workspace de uv.** Un solo lockfile y un solo entorno para todas las apps de Python, instalación muy rápida, y gestiona también la versión de Python.

## Decisión

Un monorepo con un workspace de uv. Cada aplicación de Python es un miembro del workspace (`apps/ingest`, después `apps/api`), con su propio `pyproject.toml` y el patrón `src/`.

## Consecuencias

- Un único `uv sync` prepara todo el proyecto en cualquier computadora o en el CI.
- `uv.lock` garantiza las mismas versiones en desarrollo, CI y servidores.
- Las herramientas de calidad (Ruff, mypy, pytest) se configuran una sola vez en el `pyproject.toml` raíz.
- Hay que vigilar que las apps no se acoplen demasiado entre sí: cada una solo importa lo que declara en sus dependencias.
