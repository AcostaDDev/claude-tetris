---
description: Muestra el clima actual y el pronóstico de 3 días (por defecto Cúcuta, Colombia)
argument-hint: "[ciudad]  (vacío = Cúcuta, Colombia; --local = ubicación por IP)"
allowed-tools: Skill(clima), Bash(python:*), Bash(python3:*)
---

Usa la skill `clima` para consultar el tiempo.

- Si hay argumentos, trátalos como el nombre del lugar (o `--local`): `$ARGUMENTS`
- Si no hay argumentos, usa la ciudad por defecto (Cúcuta, Colombia).

Ejecuta el script de la skill
(`.claude/skills/clima/scripts/clima.py`) con ese argumento y presenta al
usuario un resumen claro: ubicación, clima actual (temperatura, sensación,
humedad, viento, precipitación) y el pronóstico día a día.
