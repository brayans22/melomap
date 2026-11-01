# Identidad visual e interfaz de MeloMap

Referencia del diseño aprobado. El frontend (fase 8) se construye a partir de estas pantallas y de estos valores.

## Logo

| Símbolo | Logotipo |
| --- | --- |
| ![Símbolo](logo/melomap-logo.svg) | ![Logotipo](logo/melomap-wordmark.svg) |

El símbolo es un globo atravesado por una onda de sonido: **el mundo visto como una señal de audio**. Es la evolución simplificada de la propuesta 2, pensada para leerse bien desde 16 px. En el logotipo, “melo” va en negrita y “map” en peso regular, ambos en blanco.

Las dos propuestas originales se conservan en [screens/logo-propuestas.png](screens/logo-propuestas.png).

## Paleta

| Token | Valor | Uso |
| --- | --- | --- |
| `--bg` | `#08080B` | Fondo de la página |
| `--surface` | `#111116` | Tarjetas y paneles |
| `--raise` | `#18181F` | Elementos dentro de tarjetas |
| `--line` | `#25252E` | Bordes |
| `--fg` | `#F2F3F7` | Texto principal |
| `--muted` | `#9C9DAA` | Texto secundario y etiquetas |
| `--blue` | `#5B7CFF` | Acento principal, botones |
| `--peri` | `#8FA6FF` | Acento suave |
| `--sky` | `#8FE8FF` | Datos destacados, gráficos |
| `--violet` | `#A77BFF` | Segunda serie de datos |
| `--pink` | `#FF77C8` | Comparaciones y valores negativos |

Colores por género musical (mapa y gráficos): Pop `#5B7CFF`, Urbano latino `#A77BFF`, Rock `#3FB8FF`, Electrónica `#9EE7FF`, K-pop / J-pop `#FF77C8`, Afrobeats `#E6E8F5`.

**Reglas:** fondo negro liso (sin estrellas ni degradados); nada de naranja ni verde; las etiquetas en mayúsculas van en gris, no en color; el color en el texto se reserva para datos.

## Tipografía

| Rol | Fuente | Uso |
| --- | --- | --- |
| Títulos | [Sora](https://fonts.google.com/specimen/Sora) 600–700 | Encabezados y cifras grandes |
| Texto | [Instrument Sans](https://fonts.google.com/specimen/Instrument+Sans) 400–700 | Interfaz y párrafos |
| Datos | [Geist Mono](https://fonts.google.com/specimen/Geist+Mono) 400–600 | Números, BPM, códigos |

## Pantallas

- **Inicio:** mapa con cuatro modos (N.º 1 por país, viaje de una canción con línea de tiempo, mapa de calor y afinidad), canción del momento, duelo de canciones, pulso del día, quiz, comparador, cifras y ranking. [Vista superior](screens/inicio.png) · [página completa](screens/inicio-completo.jpg)
- **Ficha de canción:** huella sonora, ficha técnica, armonía, créditos, viaje por el mundo, evolución en listas y predicción. [Ver](screens/ficha-cancion.jpg)

## Idiomas

Español latino (`es-419`) como idioma principal e inglés (`en`). Formato de números de México: `1,234.5`.
