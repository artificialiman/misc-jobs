"""Extract the solved schedule into plain data, and report exactly
which subjects fell short of target and by how much -- the honest
shortfall reporting required by spec F5."""

from ortools.sat.python import cp_model
from solve import solve
from model import CLASSES, DAYS, ALL_PERIODS


def extract_schedule():
    solver, status, x, class_subjects, teachers = solve()
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"No solution found: {solver.StatusName(status)}")

    # schedule[cls][(day, period)] = list of subject ids placed there
    schedule = {cls: {} for cls in CLASSES}
    for (cls, sid, d, p), var in x.items():
        if solver.Value(var):
            schedule[cls].setdefault((d, p), []).append(sid)

    # Per-subject actual placement count vs target
    shortfalls = []
    for cls in CLASSES:
        for s in class_subjects[cls]:
            actual = sum(1 for (d, p), sids in schedule[cls].items() if s.id in sids)
            if actual < s.target_per_week:
                shortfalls.append((cls, s.name, s.id, actual, s.target_per_week))

    return solver, status, schedule, class_subjects, teachers, shortfalls


if __name__ == "__main__":
    solver, status, schedule, class_subjects, teachers, shortfalls = extract_schedule()
    print("Status:", solver.StatusName(status))
    print("Objective:", solver.ObjectiveValue())
    print()
    print("=== Shortfalls (actual < target) ===")
    if not shortfalls:
        print("None -- every subject hit its full target.")
    for cls, name, sid, actual, target in shortfalls:
        print(f"  {cls}: {name} ({sid}) = {actual}/{target}/wk  (short by {target - actual})")

    print()
    print("=== Free periods per class (regular day only, periods 1-8) ===")
    for cls in CLASSES:
        free = []
        for d in DAYS:
            for p in range(1, 9):
                if (d, p) not in schedule[cls] or not schedule[cls][(d, p)]:
                    free.append((d, p))
        print(f"  {cls}: {len(free)} free regular-day periods -> {free}")
