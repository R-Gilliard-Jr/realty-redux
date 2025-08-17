import pandas as pd

from realty_redux.Report import PropertyData, Report


def main():
    data: PropertyData = {
        "construction_year": 1928,
        "lot_size_sq_ft": 2800,
        "total_rental_size_sq_ft": 5712,
        "number_of_units": 6,
        "zoning_class": "C2",
        "unit_mix": "some text",
        "parking_spots": 0,
        "property_taxes": 18353,
        "acquisition_date": "2025-07-31",
        "asking_price": 1299999,
        "closing_cost_pct": 0.03,
        "sale_date": "2026-09-30",
        "sale_price": 1364999,
        "loan_to_value": 0.8,
        "loan_type": "Fixed",
        "loan_term": 40,
        "loan_amortization_years": 40,
        "interest_rate": 0.0735,
        "minimum_rent_coverage": 1,
        "points_paid": 1.875,
        "interest_only": "Yes",
        "interest_only_years": 10,
        "loan_costs": 3400,
        "purchase_price": 1299999,
        "renovation_cost": 50000,
        "contingency_funds": 10000,
        "rental_units": [{"initial_rent": 2400, "rent_growth": 0.05}] * 6,
        "property_management": 0.08,
        "home_insurance": 0.05,
        "ongoing_maintenance": 0.1,
        "operating_expenses": 0.2,
        "unpaid_utilities": 0.0347,
        "broker_fee_on_new_rental": 1,
        "loan_principal": 1039999,
    }
    report = Report(data).sources_and_uses().cash_flow(1)
    print(
        report.property_data["cash_flow"],
        report.property_data["cash_on_cash"],
    )
    amort = report.amortization_table()
    df = pd.DataFrame.from_records(
        list(zip(amort[0], amort[1], amort[2])),
        columns=["Interest", "Principal", "Total"],
    )
    print(df)


if __name__ == "__main__":
    main()
