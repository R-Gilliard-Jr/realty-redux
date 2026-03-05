import os
import re

import requests
from flask import Blueprint, render_template, request, jsonify

from realty_redux.common.calculations import calc_cash_flow

bp = Blueprint("index", __name__)

ASSUMPTIONS = {
    "rent_pct": 0.05,
    "down_pct": 20,
    "rate": 6.5,
    "term": 30,
    "closing_pct": 3,
    "vacancy_pct": 0,
    "tax_pct": 0,
    "ins_pct": 0,
    "maint": 0,
    "capex": 0,
    "pm_pct": 0,
    "hoa": 0,
    "util": 0,
}

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = "realty-in-us.p.rapidapi.com"


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/assumptions", methods=["GET", "POST"])
def assumptions():
    if request.method == "POST":
        for k, v in request.json.items():
            if k in ASSUMPTIONS:
                ASSUMPTIONS[k] = float(v)
    return jsonify(ASSUMPTIONS)


@bp.route("/search", methods=["POST"])
def api_search():
    q = request.json.get("query", "")
    if not q:
        return jsonify({"error": "No query"}), 400
    try:
        listings = realtor_search(q)
        for l in listings:
            if not l.get("lat") or not l.get("lng"):
                lat, lng = geocode(l["address"])
                l["lat"] = lat
                l["lng"] = lng
            l["cf"] = calc_cash_flow(l["price"], ASSUMPTIONS, l.get("reno", 0))
        msg = None
        if not listings:
            msg = "No listings found. Try a different location, zip code, or broader search."
        return jsonify({"listings": listings, "count": len(listings), "message": msg})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@bp.route("/recalc", methods=["POST"])
def api_recalc():
    listings = request.json.get("listings", [])
    for l in listings:
        l["cf"] = calc_cash_flow(l["price"], ASSUMPTIONS, l.get("reno", 0))
    return jsonify({"listings": listings})


# ─── Realtor.com Search via RapidAPI ───


def realtor_search(query):
    """Search for-sale listings using RapidAPI's Realtor.com endpoint."""
    if not RAPIDAPI_KEY:
        raise ValueError(
            "No API key configured. Get a FREE key at "
            "https://rapidapi.com/apidojo/api/realty-in-us "
            "then set RAPIDAPI_KEY in your environment or at the top of this file."
        )

    # Parse query for location, price, beds
    price_m = re.search(
        r"(?:under|below|less than)\s*\$?([\d,]+)\s*(k|m)?", query, re.I
    )
    max_price = None
    if price_m:
        p = int(price_m.group(1).replace(",", ""))
        mult = (price_m.group(2) or "").lower()
        if mult == "k":
            max_price = p * 1000
        elif mult == "m":
            max_price = p * 1000000
        else:
            max_price = p
        if max_price < 5000:
            max_price = max_price * 1000

    bed_m = re.search(r"(\d)\s*(?:bed|br|bd)", query, re.I)
    min_beds = int(bed_m.group(1)) if bed_m else None

    bath_m = re.search(r"(\d)\s*(?:bath|ba)", query, re.I)
    min_baths = int(bath_m.group(1)) if bath_m else None

    # Detect zip code
    zip_m = re.search(r"\b(\d{5})\b", query)
    zip_code = None
    if zip_m:
        candidate = zip_m.group(1)
        if not (price_m and candidate in price_m.group(0).replace(",", "")):
            zip_code = candidate

    # Clean query for location
    loc = re.sub(
        r"(?:under|below|less than|above|over|between)\s*\$?[\d,]+\s*[km]?",
        "",
        query,
        flags=re.I,
    )
    loc = re.sub(
        r"\b(homes?|houses?|condos?|apartments?|for sale|for rent|bedroom|bathrooms?|"
        r"under|below|above|over|between|near|in|around|with|and|the|cheap|affordable|"
        r"new|old|listing|listings|property|properties|real estate)\b",
        "",
        loc,
        flags=re.I,
    )
    loc = re.sub(r"[\$]", "", loc)
    loc = re.sub(r"\b\d+\s*(bed|br|bath|ba|bd)\w*", "", loc, flags=re.I)
    loc = re.sub(r"\b\d+[km]?\b", "", loc)
    loc = " ".join(loc.split()).strip().strip(",").strip()

    print(
        f"  [Realtor] Location: '{loc}' | Max price: {max_price} | Beds: {min_beds} | Zip: {zip_code}"
    )

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }

    # Build request body
    body = {
        "limit": 200,
        "offset": 0,
        "status": ["for_sale", "ready_to_build"],
        "sort": {"direction": "desc", "field": "list_date"},
    }

    if zip_code:
        body["postal_code"] = zip_code
    elif loc:
        # Try to split "City ST" or "City, ST" format
        city_state = re.match(r"^(.+?)[,\s]+([A-Z]{2})$", loc.strip(), re.I)
        if city_state:
            body["city"] = city_state.group(1).strip()
            body["state_code"] = city_state.group(2).upper()
        else:
            body["city"] = loc
    else:
        raise ValueError("Could not parse a location from your search query.")

    if max_price:
        body["price_max"] = max_price
    if min_beds:
        body["beds_min"] = min_beds
    if min_baths:
        body["baths_min"] = min_baths

    print(f"  [Realtor] API body: {body}")

    # Call the API (POST with JSON body)
    r = requests.post(
        f"https://{RAPIDAPI_HOST}/properties/v3/list",
        headers=headers,
        json=body,
        timeout=15,
    )
    print(f"  [Realtor] API status: {r.status_code}")

    if r.status_code == 429:
        raise ValueError(
            "API rate limit reached. Try again later or upgrade your RapidAPI plan."
        )
    if r.status_code == 403:
        raise ValueError("API key is invalid or expired. Check your RAPIDAPI_KEY.")
    if r.status_code != 200:
        raise ValueError(f"API error: HTTP {r.status_code}")

    data = r.json()

    # Handle both v2 and v3 response formats
    properties = data.get("data", {}).get("home_search", {}).get("results", [])
    if not properties:
        properties = data.get("data", {}).get("results", [])
    if not properties:
        properties = data.get("properties", [])
    if not properties:
        if isinstance(data.get("data"), list):
            properties = data["data"]

    print(f"  [Realtor] Raw results: {len(properties)}")

    listings = []
    for p in properties:
        try:
            listing = _parse_realtor_property(p)
            if listing:
                listings.append(listing)
        except Exception:
            continue

    # Client-side price filter (API may not enforce price_max precisely)
    if max_price:
        listings = [l for l in listings if l["price"] <= max_price]

    # Deduplicate
    seen = set()
    unique = []
    for l in listings:
        if l["address"] not in seen:
            seen.add(l["address"])
            unique.append(l)

    print(f"  [Realtor] Final: {len(unique)} listings")
    return unique


def _parse_realtor_property(p):
    """Parse a single property from the Realtor.com API response."""
    if not isinstance(p, dict):
        return None

    # v3 format: nested under location.address and description
    loc = p.get("location", {}) or {}
    addr_obj = loc.get("address", {}) or {}
    desc = p.get("description", {}) or {}
    # Coordinates are under location.address.coordinate in v3
    coord = addr_obj.get("coordinate", {}) or loc.get("coordinate", {}) or {}

    # v2 format: flat structure
    if not addr_obj and "address" in p:
        addr_obj = p["address"] if isinstance(p["address"], dict) else {}

    # Build address
    line = addr_obj.get("line", "") or p.get("address_line", "") or ""
    city = addr_obj.get("city", "") or p.get("city", "") or ""
    state = (
        addr_obj.get("state_code", "")
        or addr_obj.get("state", "")
        or p.get("state_code", "")
        or ""
    )
    zipcode = addr_obj.get("postal_code", "") or p.get("postal_code", "") or ""
    parts = [x for x in [line, city, state, zipcode] if x]
    address = ", ".join(parts)
    if not address:
        return None

    # Price
    price = p.get("list_price") or p.get("price") or desc.get("list_price")
    if isinstance(price, dict):
        price = price.get("value") or price.get("max")
    if price is None:
        return None
    price = int(float(str(price).replace(",", "")))
    if price < 10000:
        return None

    # Beds, baths, sqft
    beds = desc.get("beds") or p.get("beds")
    baths = desc.get("baths") or p.get("baths")
    sqft = desc.get("sqft") or p.get("sqft")
    if not sqft:
        bldg = p.get("building_size", {})
        if isinstance(bldg, dict):
            sqft = bldg.get("size")

    # Coordinates
    lat = coord.get("lat") or coord.get("latitude") or p.get("latitude")
    lng = (
        coord.get("lon")
        or coord.get("lng")
        or coord.get("longitude")
        or p.get("longitude")
    )

    # URL
    url = p.get("href") or p.get("rdc_web_url") or p.get("web_url") or ""
    if url and not url.startswith("http"):
        url = "https://www.realtor.com" + url

    # Summary
    summary = desc.get("text", "") or p.get("description", "")
    if isinstance(summary, dict):
        summary = summary.get("text", "")

    return {
        "address": address,
        "price": price,
        "beds": int(beds) if beds else None,
        "baths": int(float(str(baths))) if baths else None,
        "sqft": int(float(str(sqft))) if sqft else None,
        "lat": float(lat) if lat else None,
        "lng": float(lng) if lng else None,
        "url": url or None,
        "summary": (str(summary) or "")[:200],
        "reno": 0,
    }


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
