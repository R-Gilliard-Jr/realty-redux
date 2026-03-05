import os
import re
import traceback

import requests
from flask import Blueprint, render_template, request, jsonify

from realty_redux.common.calculations import calc_cash_flow
from realty_redux.external.realtor_dot_com import RealtorDotCom
from realty_redux.external.geocode import geocode

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

rdc = RealtorDotCom()


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

@bp.route("/advanced-search", methods=["POST"])
def advanced_search():
    payload = request.json
    payload = {key: value for key, value in payload.items() if value}
    try:
        listings = RealtorDotCom().search(payload)
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
       traceback.print_exc()
       return jsonify({"error": str(e)}), 500

@bp.route("/advanced-settings", methods=["GET"])
def advanced_settings():
    return jsonify([RealtorDotCom.searchOptions, RealtorDotCom.entry])

@bp.route("/search", methods=["POST"])
def api_search():
    q = request.json.get("query", "")
    if not q:
        return jsonify({"error": "No query"}), 400
    try:
        listings = rdc.realtor_search(q)
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
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@bp.route("/recalc", methods=["POST"])
def api_recalc():
    listings = request.json.get("listings", [])
    for l in listings:
        l["cf"] = calc_cash_flow(l["price"], ASSUMPTIONS, l.get("reno", 0))
    return jsonify({"listings": listings})