#!/usr/bin/env python3
"""Clima actual y pronóstico usando Open-Meteo (sin API key, solo stdlib).

Uso:
    python clima.py                 # ciudad por defecto: Cúcuta, Colombia
    python clima.py Madrid          # ciudad concreta
    python clima.py "Buenos Aires"  # nombres con espacios
    python clima.py Lima Peru       # varios términos = un solo nombre
    python clima.py --local         # ubicación local (por IP)
"""

# Ciudad usada cuando no se pasa ningún argumento.
CIUDAD_POR_DEFECTO = "Cúcuta, Colombia"
import json
import sys
import urllib.parse
import urllib.request

# En Windows la consola suele usar cp1252; forzamos UTF-8 para los acentos y °.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

# Descripción de los códigos WMO (weather_code) en español.
WMO = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna densa",
    56: "Llovizna helada ligera",
    57: "Llovizna helada densa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    66: "Lluvia helada ligera",
    67: "Lluvia helada fuerte",
    71: "Nieve ligera",
    73: "Nieve moderada",
    75: "Nieve fuerte",
    77: "Granos de nieve",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros",
    86: "Chubascos de nieve fuertes",
    95: "Tormenta",
    96: "Tormenta con granizo ligero",
    99: "Tormenta con granizo fuerte",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "clima-skill/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def geocode(nombre):
    q = urllib.parse.urlencode(
        {"name": nombre, "count": 1, "language": "es", "format": "json"}
    )
    data = fetch(f"https://geocoding-api.open-meteo.com/v1/search?{q}")
    results = data.get("results")
    if not results:
        sys.exit(f"No se encontró la ubicación: {nombre}")
    r = results[0]
    etiqueta = ", ".join(
        x for x in (r.get("name"), r.get("admin1"), r.get("country")) if x
    )
    return r["latitude"], r["longitude"], etiqueta


def ubicacion_local():
    try:
        data = fetch(
            "http://ip-api.com/json/?fields=status,message,city,regionName,country,lat,lon"
        )
    except Exception as e:  # noqa: BLE001
        sys.exit(
            f"No se pudo detectar la ubicación local ({e}). "
            "Pasa el nombre de la ciudad como argumento."
        )
    if data.get("status") != "success":
        sys.exit(
            f"No se pudo detectar la ubicación local: {data.get('message', 'error')}. "
            "Pasa el nombre de la ciudad como argumento."
        )
    etiqueta = ", ".join(
        x for x in (data.get("city"), data.get("regionName"), data.get("country")) if x
    )
    return data["lat"], data["lon"], etiqueta


def clima(lat, lon):
    q = urllib.parse.urlencode(
        {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                ]
            ),
            "timezone": "auto",
            "forecast_days": 3,
        }
    )
    return fetch(f"https://api.open-meteo.com/v1/forecast?{q}")


def main():
    args = sys.argv[1:]
    if args and args[0] in ("--local", "-l", "local"):
        lat, lon, etiqueta = ubicacion_local()
    elif args:
        lat, lon, etiqueta = geocode(" ".join(args))
    else:
        lat, lon, etiqueta = geocode(CIUDAD_POR_DEFECTO)

    data = clima(lat, lon)
    c = data["current"]
    desc = WMO.get(c["weather_code"], f"código {c['weather_code']}")

    print(f"[UBICACION] {etiqueta}")
    print(f"   {float(lat):.2f}, {float(lon):.2f} · zona horaria {data.get('timezone')}")
    print()
    print(
        f"[AHORA] {c['temperature_2m']}°C "
        f"(sensación {c['apparent_temperature']}°C) · {desc}"
    )
    print(
        f"   Humedad {c['relative_humidity_2m']}% · "
        f"viento {c['wind_speed_10m']} km/h · "
        f"precipitación {c['precipitation']} mm"
    )
    print()
    print("[PRONOSTICO 3 DIAS]")
    d = data["daily"]
    for i, fecha in enumerate(d["time"]):
        dd = WMO.get(d["weather_code"][i], f"código {d['weather_code'][i]}")
        print(
            f"  {fecha}: {d['temperature_2m_min'][i]}–{d['temperature_2m_max'][i]}°C · "
            f"prob. lluvia {d['precipitation_probability_max'][i]}% · {dd}"
        )


if __name__ == "__main__":
    main()
