import json

from flask import Blueprint, request

from realty_redux.Report import Report

bp = Blueprint("report", __name__, url_prefix="/report")


@bp.route("/", methods=["POST"])
def index():
    report = (
        Report(request.get_json()).sources_and_uses().cash_flow(1).amortization_table()
    )

    return json.dumps(report)
