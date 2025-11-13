"""
static_lco_model.py
--------------------
Standalone static 2–tier Lexicographic Constraint Optimization (LCO) demo
for hotel bookings using Pyomo.

Tier L2: maximize expected revenue
Tier L3: minimize expected overbooking slack subject to the L2 revenue floor.

This module is designed to be used both locally and inside Google Colab.
It matches the mathematical structure described in the LCO papers/notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional

try:
    from pyomo.environ import (
        ConcreteModel, Set, Param, Var,
        Binary, NonNegativeReals,
        Constraint, Objective, maximize, minimize,
        value, SolverFactory
    )
except ImportError as e:
    raise ImportError(
        "Pyomo is required to use static_lco_model.py. "
        "Install it via `pip install pyomo highspy`."
    ) from e


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BookingSpec:
    start_day: int
    length_of_stay: int
    price_per_night: float
    show_prob: float


@dataclass
class LCOResult:
    revenue_L2: float
    slack_L3: float
    accepted_bookings: List[int]
    room_assignments: Dict[int, Tuple[Optional[int], List[int]]]
    slack_by_day: Dict[int, float]


# ---------------------------------------------------------------------------
# Synthetic data (matches the paper / Colab examples)
# ---------------------------------------------------------------------------

def build_default_bookings() -> Dict[int, BookingSpec]:
    """Return the 12–booking toy dataset used in the paper/notebook.

    Keys are booking IDs 1..12.
    """
    raw = {
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
    return {
        b: BookingSpec(*vals)
        for b, vals in raw.items()
    }


# ---------------------------------------------------------------------------
# Core Pyomo model builder
# ---------------------------------------------------------------------------

def build_static_lco_model(
    bookings: Optional[Dict[int, BookingSpec]] = None,
    days: int = 5,
    rooms: int = 10,
    capacity_by_day: Optional[Dict[int, int]] = None,
):
    """Build the static 2–tier LCO Pyomo model.

    Parameters
    ----------
    bookings : dict[int, BookingSpec], optional
        Mapping booking_id -> BookingSpec. If None, uses the default 12–booking toy set.
    days : int
        Number of days in the horizon (default 5).
    rooms : int
        Number of rooms (default 10).
    capacity_by_day : dict[int, int], optional
        Capacity per day. If None, uses `rooms` for every day.

    Returns
    -------
    m : ConcreteModel
        A Pyomo model with Tier L2 objective (revenue maximization) set.
    """
    if bookings is None:
        bookings = build_default_bookings()

    m = ConcreteModel()

    # ---- Sets
    m.D = Set(initialize=list(range(1, days + 1)))
    m.R = Set(initialize=list(range(1, rooms + 1)))
    m.B = Set(initialize=list(bookings.keys()))

    # ---- Parameters
    m.start = Param(
        m.B,
        initialize={b: spec.start_day for b, spec in bookings.items()},
        within=m.D
    )
    m.length = Param(
        m.B,
        initialize={b: spec.length_of_stay for b, spec in bookings.items()},
    )
    m.price = Param(
        m.B,
        initialize={b: spec.price_per_night for b, spec in bookings.items()},
    )
    m.showp = Param(
        m.B,
        initialize={b: spec.show_prob for b, spec in bookings.items()},
    )

    if capacity_by_day is None:
        capacity_by_day = {d: rooms for d in range(1, days + 1)}
    m.cap = Param(m.D, initialize=capacity_by_day)

    # Helper: stay-days for each booking
    def _stay_days(b):
        s = int(m.start[b])
        L = int(m.length[b])
        return [d for d in m.D if d >= s and d < s + L]

    instay = {(b, d) for b in m.B for d in m.D if d in _stay_days(b)}
    m.InStay = Set(dimen=2, initialize=instay)

    yidx = {(b, r, d) for (b, d) in instay for r in m.R}
    m.YIDX = Set(dimen=3, initialize=yidx)

    cont = {
        (b, r, d)
        for b in m.B
        for r in m.R
        for d in m.D
        if (b, d) in instay and (b, d + 1) in instay
    }
    m.ContPair = Set(dimen=3, initialize=cont)

    # ---- Variables
    m.a = Var(m.B, within=Binary)               # accept booking
    m.y = Var(m.YIDX, within=Binary)            # assignment
    m.w = Var(m.D, within=NonNegativeReals)     # overbooking slack per day

    # ---- Constraints

    # 1) Room exclusivity
    def room_excl(m, r, d):
        return sum(
            m.y[b, r, d] for b in m.B
            if (b, d) in m.InStay
        ) <= 1

    m.RoomExcl = Constraint(m.R, m.D, rule=room_excl)

    # 2) Acceptance/assignment link
    def assign_link(m, b, d):
        if (b, d) not in m.InStay:
            return Constraint.Skip
        return sum(m.y[b, r, d] for r in m.R) == m.a[b]

    m.Assign = Constraint(m.B, m.D, rule=assign_link)

    # 3) Continuity
    def continuity(m, b, r, d):
        return m.y[b, r, d] == m.y[b, r, d + 1]

    m.Continuity = Constraint(m.ContPair, rule=continuity)

    # 4) Overbooking slack (expected shows vs capacity)
    def overbooking(m, d):
        exp_shows = sum(
            m.a[b] * m.showp[b]
            for b in m.B
            if (b, d) in m.InStay
        )
        return m.w[d] >= exp_shows - m.cap[d]

    m.Overbook = Constraint(m.D, rule=overbooking)

    # ---- Tier L2 objective: maximize revenue
    m.RevExpr = sum(
        m.a[b] * m.price[b] * m.length[b]
        for b in m.B
    )
    m.obj = Objective(expr=m.RevExpr, sense=maximize)

    return m


# ---------------------------------------------------------------------------
# Two–tier solve: L2 then L3
# ---------------------------------------------------------------------------

def solve_two_tier_lco(
    bookings: Optional[Dict[int, BookingSpec]] = None,
    days: int = 5,
    rooms: int = 10,
    capacity_by_day: Optional[Dict[int, int]] = None,
    solver_name: str = "highs",
    revenue_floor_tolerance: float = 1e-6,
) -> LCOResult:
    """Solve the 2–tier LCO problem (L2 -> L3) and return a compact result.

    This routine:

    1. Builds the static model.
    2. Solves Tier L2 (maximize revenue) and records Z2*.
    3. Injects a revenue floor Rev >= Z2* - eps.
    4. Switches to Tier L3 objective: minimize sum_d w[d].
    5. Solves Tier L3 and extracts key metrics.
    """
    m = build_static_lco_model(
        bookings=bookings,
        days=days,
        rooms=rooms,
        capacity_by_day=capacity_by_day,
    )

    opt = SolverFactory(solver_name)

    # ---- Tier L2: max revenue
    res_L2 = opt.solve(m, tee=False)
    Z2 = value(m.RevExpr)

    # ---- Inject revenue floor and switch to Tier L3
    m.RevenueFloor = Constraint(expr=m.RevExpr >= Z2 - revenue_floor_tolerance)
    m.del_component(m.obj)
    m.obj = Objective(expr=sum(m.w[d] for d in m.D), sense=minimize)

    res_L3 = opt.solve(m, tee=False)

    # ---- Extract results
    slack_by_day = {int(d): float(value(m.w[d])) for d in m.D}
    slack_sum = sum(slack_by_day.values())

    accepted_bookings = [int(b) for b in m.B if value(m.a[b]) > 0.5]

    # Determine a single room per booking (if assigned consistently)
    # and its stay-days.
    def _stay_days_local(b):
        s = int(m.start[b])
        L = int(m.length[b])
        return [d for d in m.D if d >= s and d < s + L]

    room_assignments: Dict[int, Tuple[Optional[int], List[int]]] = {}
    for b in accepted_bookings:
        sdays = _stay_days_local(b)
        chosen_room = None
        for r in m.R:
            ok = True
            for d in sdays:
                if (b, r, d) not in m.YIDX or value(m.y[b, r, d]) <= 0.5:
                    ok = False
                    break
            if ok:
                chosen_room = int(r)
                break
        room_assignments[int(b)] = (chosen_room, [int(d) for d in sdays])

    return LCOResult(
        revenue_L2=float(Z2),
        slack_L3=float(slack_sum),
        accepted_bookings=accepted_bookings,
        room_assignments=room_assignments,
        slack_by_day=slack_by_day,
    )


# ---------------------------------------------------------------------------
# Simple CLI entry point
# ---------------------------------------------------------------------------

def _format_assignments(assignments: Dict[int, Tuple[Optional[int], List[int]]]) -> str:
    lines = []
    for b, (room, days) in sorted(assignments.items()):
        if room is None:
            lines.append(f"  - Booking {b}: accepted, room assignment not unique")
        else:
            span = ",".join(str(d) for d in days)
            lines.append(f"  - Booking {b}: room {room}, days [{span}]")
    return "\n".join(lines)


if __name__ == "__main__":
    print("=== Static 2–Tier LCO Demo ===")
    result = solve_two_tier_lco()

    print(f"Tier L2 revenue optimum Z2* = {result.revenue_L2:.2f}")
    print(f"Tier L3 total overbooking slack = {result.slack_L3:.4f}")
    print("Slack by day:")
    for d, w in sorted(result.slack_by_day.items()):
        print(f"  Day {d}: w_d = {w:.4f}")

    print("\nAccepted bookings and assignments:")
    print(_format_assignments(result.room_assignments))
