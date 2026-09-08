---
name: clima
description: Consulta el clima actual y el pronóstico de 3 días. Por defecto usa Cúcuta, Colombia; acepta cualquier ciudad o la ubicación local (por IP). Usa la API gratuita de Open-Meteo sin API key. Úsala cuando el usuario pida el clima, el tiempo, la temperatura o el pronóstico.
---

# Clima

Obtiene datos meteorológicos desde la línea de comandos con
`.claude/skills/clima/scripts/clima.py`. El script solo usa la librería estándar
de Python: sin dependencias, sin instalación y sin API key.

**Ciudad por defecto: Cúcuta, Colombia** (cuando no se pasan argumentos).

## Uso

Ciudad por defecto (Cúcuta, Colombia):

```bash
python ".claude/skills/clima/scripts/clima.py"
```

Una ciudad concreta (pasa el nombre como argumentos):

```bash
python ".claude/skills/clima/scripts/clima.py" Madrid
python ".claude/skills/clima/scripts/clima.py" "Buenos Aires"
python ".claude/skills/clima/scripts/clima.py" Lima Peru
```

Ubicación local (detectada por IP):

```bash
python ".claude/skills/clima/scripts/clima.py" --local
```

En Windows usa `python`; en macOS/Linux quizá necesites `python3`.

## Qué hace

1. Sin argumentos usa la ciudad por defecto (Cúcuta, Colombia). Con un nombre de
   lugar lo geocodifica con la API de geocoding de Open-Meteo
   (`geocoding-api.open-meteo.com`). Con `--local` detecta la ubicación
   aproximada por IP con `ip-api.com`.
2. Pide el clima actual y el pronóstico diario (3 días) a
   `api.open-meteo.com/v1/forecast` con `timezone=auto`.
3. Imprime temperatura, sensación térmica, humedad, viento y precipitación
   actuales, más el pronóstico día a día, con las descripciones de los códigos
   WMO en español.

Presenta el resultado al usuario de forma resumida y clara.

## Notas

- Requiere conexión a internet.
- `ip-api.com` (solo con `--local`) va por HTTP y puede estar bloqueado en
  algunas redes o VPN; si falla, pasa el nombre de la ciudad como argumento.
- Para cambiar la ciudad por defecto, edita `CIUDAD_POR_DEFECTO` en
  `scripts/clima.py`.
- Todas las APIs usadas son gratuitas y no requieren registro.
