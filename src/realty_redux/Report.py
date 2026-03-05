from typing import Self, TypedDict


class RentalUnit(TypedDict):
    rent_growth: float
    initial_rent: float


class PropertyData(TypedDict):
    construction_year: int
    lot_size_sq_ft: int
    total_rental_size_sq_ft: int
    number_of_units: int
    zoning_class: str
    unit_mix: str
    parking_spots: int
    property_taxes: float
    acquisition_date: str
    asking_price: float
    closing_cost_pct: float
    sale_date: str
    sale_price: float
    loan_to_value: float
    loan_type: str
    loan_term: int
    loan_amortization_years: int
    interest_rate: float
    minimum_rent_coverage: float
    points_paid: float
    interest_only: str
    interest_only_years: int
    loan_costs: float
    purchase_price: float
    renovation_cost: float
    loan_costs: float
    contingency_funds: float
    rental_units: list[RentalUnit]
    property_management: float
    home_insurance: float
    ongoing_maintenance: float
    operating_expenses: float
    unpaid_utilities: float
    broker_fee_on_new_rental: float
    loan_principal: float


class Report:
    def __init__(self, property_data: dict):
        self.property_data = PropertyData(property_data)

    def sources_and_uses(self) -> Self:
        property_data = self.property_data

        # Sources and uses
        debt = property_data["purchase_price"] * property_data["loan_to_value"]
        closing_costs = (
            property_data["closing_cost_pct"] * property_data["purchase_price"]
        )
        points_purchased = property_data["points_paid"] / 100 * debt

        # Totals
        total_uses = (
            property_data["purchase_price"]
            + closing_costs
            + points_purchased
            + property_data["renovation_cost"]
            + property_data["loan_costs"]
            + property_data["contingency_funds"]
        )
        equity_from_buyers = total_uses - debt
        total_sources = total_uses

        property_data.update(
            {
                "debt": debt,
                "closing_costs": closing_costs,
                "points_purchased": points_purchased,
                "total_uses": total_uses,
                "equity_from_buyers": equity_from_buyers,
                "total_sources": total_sources,
            }
        )

        return self

    def calculate_rental_revenue(self, year: int):
        pass

    def cash_flow(self, month: int) -> Self:
        property_data = self.property_data
        units = property_data["rental_units"]

        revenue = sum(
            [
                unit["initial_rent"] * unit["rent_growth"] ** (month // 12)
                for unit in units
            ]
        )

        property_manager = revenue * property_data["property_management"]
        unpaid_utilities = revenue * property_data["unpaid_utilities"]
        property_taxes = property_data["property_taxes"] / 12
        home_insurance = revenue * property_data["home_insurance"]
        maintenance = revenue * property_data["ongoing_maintenance"]
        operating_expenses = revenue * property_data["operating_expenses"]

        # TODO: Need to handle one-time expenditure/infusions
        broker_fee = 0
        investment_cash_flow = 0

        net_operating_income = (
            revenue
            - property_manager
            - unpaid_utilities
            - property_taxes
            - home_insurance
            - maintenance
            - operating_expenses
            - broker_fee
        )

        # TODO: Should the denominator here be different?
        cap_rate = net_operating_income / property_data["asking_price"]

        amortization_table = self.amortization_table()
        debt_service = amortization_table[2][month]

        cash_flow = net_operating_income - debt_service + investment_cash_flow
        cash_on_cash = cash_flow * 12 / property_data["equity_from_buyers"]
        rent_coverage = revenue / debt_service
        covenant = rent_coverage > property_data["minimum_rent_coverage"]

        # TODO: Calculate IRR which involves first calculating cash flow into the future
        # then also calculating months into the future
        # irr = xirr()
        irr = 0

        property_data.update(
            {
                "cash_flow": cash_flow,
                "cap_rate": cap_rate,
                "debt_service": debt_service,
                "property_manager": property_manager,
                "unpaid_utilities": unpaid_utilities,
                "property_taxes": property_taxes,
                "home_insurance": home_insurance,
                "maintenance": maintenance,
                "operating_expenses": operating_expenses,
                "cash_on_cash": cash_on_cash,
                "covenant": covenant,
                "rent_coverage": rent_coverage,
                "irr": irr,
            }
        )

        return self

    def amortization_table(self) -> Self:
        interest = principal = 0.0
        interest_only = self.property_data["interest_only"]
        interest_rate = self.property_data["interest_rate"]
        loan_amortization_years = self.property_data["loan_amortization_years"]
        interest_only_years = self.property_data["interest_only_years"]
        loan_principal = self.property_data["loan_principal"]
        monthly_interest = interest_rate / 12
        total_payments = loan_amortization_years * 12

        interest = []
        principal = []
        monthly_interest = interest_rate / 12
        total_payments = principal_payments = loan_amortization_years * 12
        payment_no = 1

        if interest_only:
            principal_payments = (loan_amortization_years - interest_only_years) * 12

        payment = (
            loan_principal
            * (monthly_interest * (1 + monthly_interest) ** principal_payments)
            / (((1 + monthly_interest) ** principal_payments) - 1)
        )

        while total_payments:
            principal_payment = 0
            interest_payment = monthly_interest * loan_principal
            interest.append(interest_payment)

            if payment_no > interest_only_years * 12 or not interest_only:
                principal_payment = payment - interest_payment
                principal.append(principal_payment)
            else:
                principal.append(0)

            payment_no += 1
            total_payments -= 1
            loan_principal -= principal_payment

        total = [sum(t) for t in zip(interest, principal)]

        return interest, principal, total


if __name__ == "__main__":
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
    print(report.property_data["cash_flow"], report.property_data["cash_on_cash"])
