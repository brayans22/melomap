# Política de seguridad

## Reportar una vulnerabilidad

Si encuentras un problema de seguridad, **no abras un issue público**. Usa la opción
[Report a vulnerability](https://docs.github.com/es/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
del repositorio en GitHub (pestaña *Security*). Responderé en un máximo de 7 días.

## Prácticas que sigue el proyecto

- Ningún secreto en el código: variables de entorno, `.env` ignorado por Git y `.env.example` sin valores.
- `gitleaks` en pre-commit y en el CI para bloquear contraseñas y tokens.
- Dependencias fijadas en `uv.lock` y actualizadas con Dependabot.
- Workflows de GitHub Actions con permisos mínimos (`contents: read`).
- La administración de los servidores solo es accesible por VPN; el sitio público sale por Cloudflare Tunnel.
- Cada usuario y servicio tiene solo los permisos que necesita.
