import requests

def geocode(addr):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": addr, "format": "json", "limit": 1},
            headers={"User-Agent": "CashFlowApp/1.0"},
            timeout=5,
        )
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"])
    except Exception:
        pass
    return None, None