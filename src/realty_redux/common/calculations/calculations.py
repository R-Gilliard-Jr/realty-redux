def calc_cash_flow(price, a, reno=0, custom_rent=None):
    down = price * a["down_pct"] / 100
    loan = price - down
    closing = price * a["closing_pct"] / 100
    inv = down + closing + reno
    mr = a["rate"] / 100 / 12
    n = a["term"] * 12
    if loan > 0 and mr > 0:
        mort = loan * (mr * (1 + mr) ** n) / ((1 + mr) ** n - 1)
    else:
        mort = 0
    if custom_rent is not None:
        rent = custom_rent
    else:
        rent = price * a["rent_pct"] / 12
    vac = rent * a["vacancy_pct"] / 100
    eff = rent - vac
    tax = price * a["tax_pct"] / 100 / 12
    ins = price * a["ins_pct"] / 100 / 12
    pm = rent * a["pm_pct"] / 100
    exp = mort + tax + ins + a["maint"] + a["capex"] + pm + a["hoa"] + a["util"]
    mcf = eff - exp
    acf = mcf * 12
    if inv > 0:
        coc = acf / inv * 100
    else:
        coc = 0
    noi = (
        eff * 12
        - (tax + ins + a["maint"] + a["capex"] + pm + a["hoa"] + a["util"]) * 12
    )
    if price > 0:
        cap = noi / price * 100
    else:
        cap = 0
    if mort > 0:
        dscr = eff / mort
    else:
        dscr = 0
    return {
        "mort": round(mort, 2),
        "rent": round(rent, 2),
        "mcf": round(mcf, 2),
        "acf": round(acf, 2),
        "coc": round(coc, 2),
        "cap": round(cap, 2),
        "dscr": round(dscr, 2),
        "inv": round(inv, 2),
        "down": round(down, 2),
        "loan": round(loan, 2),
    }
