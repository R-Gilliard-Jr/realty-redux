import json

import pandas as pd
from flask import Blueprint, request

from realty_redux.Report import Report

bp = Blueprint("report", __name__, url_prefix="/report")


@bp.route("/", methods=["POST"])
def index():
    report = Report(request.get_json()).sources_and_uses().cash_flow(1)
    amortization_table = report.amortization_table()
    amortization_df = pd.DataFrame.from_records(
        list(zip(amortization_table[0], amortization_table[1], amortization_table[2])),
        columns=["Interest", "Principal", "Total"],
    )

    return amortization_df.to_html()
