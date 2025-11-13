"""
pyomo_lco_mini.py
------------------
Minimal Lexicographic Constraint Optimization (LCO) demo:
 - Tier L2: maximize expected revenue
 - Tier L3: minimize expected overbooking slack with a revenue floor

This is the same 10-rooms × 5-days example described in the LCO hotel paper.
It is designed to be:
 - Small enough to run quickly on a laptop
 - Clear enough to inspect and adapt

Usage
-----
    pip install pyomo highspy
    # or: pip install pyomo && apt-get install -y coinor-cbc (Linux/Debian)

    python pyomo_lco_mini.py

By default the script will try to use HiGHS; if unavailable, it will
fall back to CBC if installed.
"""

from pyomo.environ import (
    ConcreteModel, Set, Var, Param, Binary, NonNegativeReals,
    Constraint, Objective, maximize, minimize, value, SolverFactory
)

# ---------------------------------------------------------------------
# Synthetic toy instance: 10 rooms × 5 days, 12 bookings
# ---------------------------------------------------------------------

DAYS = 5
ROOMS = 10
days = list(range(1, DAYS + 1))
rooms = list(range(1, ROOMS + 1))

# Daily capacity (Cap_d); here, constant = ROOMS for all d
CAP = {d: ROOMS for d in days}

# 12 bookings with (start_day, length_of_stay, price_per_night, show_prob)
bookings = {
    1:  (1, 2, 120, 0.92),
    2:  (1, 3, 110, 0.85),
    3:  (2, 2, 150, 0.90),
    4:  (2, 3, 130, 0.80),
    5:  (3, 2, 140, 0.88),
    6:  (3, 3, 100, 0.83),
    7:  (4, 2, 160, 0.87),
    8:  (4, 2, 115, 0.78),
    9:  (5, 1, 200, 0.95),
    10: (1, 1, 180, 0.90),
    11: (2, 1, 170, 0.82),
    12: (3, 1, 175, 0.89),
}


def stay_days(bid):
    """Return the list of stay-days for booking `bid` within the 5-day horizon."""
    s, L, _, _ = bookings[bid]
    return list(range(s, min(s + L, DAYS + 1)))


B = list(bookings.keys())


# ---------------------------------------------------------------------
# Model builder
# ---------------------------------------------------------------------
def build_model():
    """Build the two-tier LCO Pyomo model.

    Tier L2: Revenue maximization (objective initially)
    Tier L3: Overbooking slack minimization (activated after adding revenue floor)
    """
    m = ConcreteModel()

    # Sets
    m.B = Set(initialize=B)
    m.R = Set(initialize=rooms)
    m.D = Set(initialize=days)

    # Parameters
    m.start = Param(m.B, initialize={b: bookings[b][0] for b in B})
    m.len = Param(m.B, initialize={b: bookings[b][1] for b in B})
    m.price = Param(m.B, initialize={b: bookings[b][2] for b in B})
    m.showp = Param(m.B, initialize={b: bookings[b][3] for b in B})
    m.cap = Param(m.D, initialize=CAP)

    # Helper sets
    # (b, d) where d is in the stay of b
    in_stay = {(b, d) for b in B for d in days if d in stay_days(b)}
    m.InStay = Set(dimen=2, initialize=in_stay)

    # Triples (b, r, d) only when (b, d) is in stay; avoids unconstrained y's
    yidx = {(b, r, d) for (b, d) in in_stay for r in rooms}
    m.YIDX = Set(dimen=3, initialize=yidx)

    # (b, r, d) pairs for continuity when both d and d+1 are in the stay of b
    cont = {
        (b, r, d)
        for b in B
        for r in rooms
        for d in days
        if d in stay_days(b) and (d + 1) in stay_days(b)
    }
    m.ContPair = Set(dimen=3, initialize=cont)

    # Variables
    m.a = Var(m.B, within=Binary)  # accept booking
    m.y = Var(m.YIDX, within=Binary)  # assignment (only valid (b, r, d))
    m.w = Var(m.D, within=NonNegativeReals)  # overbooking slack per day

    # Constraints
    # 1) Room exclusivity per day: each room at most one booking among those staying that day
    def room_excl(m, r, d):
        return sum(m.y[b, r, d] for b in m.B if (b, d) in m.InStay) <= 1

    m.RoomExcl = Constraint(m.R, m.D, rule=room_excl)

    # 2) If booking accepted, exactly one room each stay day (link acceptance to assignment)
    def assign_if_accepted(m, b, d):
        if (b, d) not in m.InStay:
            return Constraint.Skip
        return sum(m.y[b, r, d] for r in m.R) == m.a[b]

    m.Assign = Constraint(m.B, m.D, rule=assign_if_accepted)

    # 3) Continuity: same room across consecutive stay days
    def continuity(m, b, r, d):
        return m.y[b, r, d] == m.y[b, r, d + 1]

    m.Continuity = Constraint(m.ContPair, rule=continuity)

    # 4) Overbooking slack (capacity-based, consistent with the paper):
    #    w[d] >= expected_shows[d] - Cap_d, with w[d] >= 0 by variable domain
    def overbook_slack(m, d):
        expected = sum(m.a[b] * m.showp[b] for b in m.B if (b, d) in m.InStay)
        return m.w[d] >= expected - m.cap[d]

    m.OverbookSlack = Constraint(m.D, rule=overbook_slack)

    # Objective (Tier L2 by default): maximize total expected revenue over accepted bookings
    m.RevenueExpr = sum(m.a[b] * m.price[b] * m.len[b] for b in m.B)
    m.obj = Objective(expr=m.RevenueExpr, sense=maximize)

    return m


# ---------------------------------------------------------------------
# Solver helper
# ---------------------------------------------------------------------
def get_solver():
    """Try HiGHS first, then CBC. Raise error if neither is available."""
    for name in ("highs", "cbc"):
        try:
            solver = SolverFactory(name)
            # This may fail if the executable is not present
            if solver.available(exception_flag=False):
                return solver
        except Exception:
            continue
    raise RuntimeError(
        "No suitable MILP solver found. "
        "Install either HiGHS (highspy) or CBC and ensure it is on PATH."
    )


# ---------------------------------------------------------------------
# Two-tier solve: L2 then L3
# ---------------------------------------------------------------------
def run_two_tier_demo(eps=1e-6, verbose=True):
    """Run Tier L2 (revenue) then Tier L3 (overbooking slack) with a revenue floor.

    Parameters
    ----------
    eps : float
        Small tolerance for the revenue floor: Rev >= Z2* - eps.
    verbose : bool
        If True, prints summary results to stdout.

    Returns
    -------
    dict
        {
            "Z2": optimal revenue at Tier L2,
            "slack_sum": total overbooking slack at Tier L3,
            "daily_slack": {day: slack},
            "accepted_bookings": [(b, stay_days, room), ...]
        }
    """
    m = build_model()
    solver = get_solver()

    # Tier L2: maximize revenue
    res2 = solver.solve(m, tee=False)
    Z2 = value(m.RevenueExpr)

    # Inject revenue floor and switch to Tier L3: minimize sum of w[d]
    m.RevenueFloor = Constraint(expr=m.RevenueExpr >= Z2 - eps)
    m.del_component(m.obj)
    m.obj = Objective(expr=sum(m.w[d] for d in m.D), sense=minimize)

    res3 = solver.solve(m, tee=False)
    slack_sum = sum(value(m.w[d]) for d in m.D)
    daily_slack = {d: float(value(m.w[d])) for d in m.D}

    # Extract accepted bookings and room assignments
    assignments = []
    for b in m.B:
        if value(m.a[b]) > 0.5:
            sdays = stay_days(int(b))
            assigned_r = None
            for r in m.R:
                ok = True
                for d in sdays:
                    key = (int(b), int(r), int(d))
                    if key not in m.YIDX or value(m.y[key]) <= 0.5:
                        ok = False
                        break
                if ok:
                    assigned_r = int(r)
                    break
            assignments.append((int(b), sdays, assigned_r))

    result = {
        "Z2": float(Z2),
        "slack_sum": float(slack_sum),
        "daily_slack": daily_slack,
        "accepted_bookings": assignments,
    }

    if verbose:
        print("=== Two-Tier LCO Mini Demo ===")
        print(f"Tier L2 (Revenue) optimum Z2* = {result['Z2']:.2f}")
        print(f"Tier L3 (Overbooking slack) total = {result['slack_sum']:.4f}")
        print("Daily slack per day:")
        for d in days:
            print(f"  Day {d}: w_d = {result['daily_slack'][d]:.4f}")
        print("\nAccepted bookings and assigned room:")
        for b, sdays, r in result["accepted_bookings"]:
            print(f"  Booking {b}: stay_days={sdays}, room={r}")

    return result


# ---------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    run_two_tier_demo()
