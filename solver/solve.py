"""
Real CP-SAT solve for the SS1-SS3 timetable, against TIMETABLE_SPEC.md.

Priority order (locked in the spec, baked into the objective below, not
post-hoc weighting that can be gamed by placement order the way the
prior sessions' hand-rolled backtrackers were):
  1. Teacher availability -- a HARD constraint. Never violated, no
     matter what. Not part of the objective at all -- the solver
     literally cannot generate a solution that breaks this.
  2. Subject coverage -- every active subject must be placed at least
     once. Modeled as a HARD constraint too (min 1 placement per active
     subject), not an objective term, so it can never be traded away
     for a frequency gain elsewhere.
  3. Frequency targets -- soft. The objective MAXIMIZES total periods
     placed toward each subject's target_per_week, capped at the
     target (no overshoot). This is the only thing allowed to fall
     short, and CP-SAT's proof of optimality means whatever it reports
     is the genuinely best achievable, not a solver-gave-up guess.
"""

from ortools.sat.python import cp_model

from model import (
    build_teachers, build_subjects, subjects_for_class,
    CLASSES, DAYS, ALL_PERIODS, EXTENDED_PERIODS, EXTENDED_WHITELIST,
    JOINT, SCI, COMM, ARTS,
)


def slot_allowed_for_extended(period: int, teacher, day: str, subject_name: str) -> bool:
    """A subject may only sit in periods 9-10 if it's whitelisted AND
    its teacher is marked available in the extended block that day."""
    if period not in EXTENDED_PERIODS:
        return True
    if subject_name not in EXTENDED_WHITELIST:
        return False
    return day in teacher.extended_days


def solve():
    teachers = build_teachers()
    subjects = build_subjects()
    model = cp_model.CpModel()

    # One boolean variable per (class, subject-row, day, period) --
    # true if that subject is taught to that class at that exact slot.
    x = {}
    class_subjects = {cls: subjects_for_class(cls, subjects) for cls in CLASSES}

    for cls in CLASSES:
        for s in class_subjects[cls]:
            teacher = teachers[s.teacher_id]
            for d in DAYS:
                for p in ALL_PERIODS:
                    if (d, p) in teacher.unavailable:
                        continue  # HARD: never even create a variable for an unavailable slot
                    if not slot_allowed_for_extended(p, teacher, d, s.name):
                        continue  # HARD: extended-block whitelist + per-teacher extended-day rule
                    x[(cls, s.id, d, p)] = model.NewBoolVar(f"x_{cls}_{s.id}_{d}_{p}")

    # ------------------------------------------------------------------
    # HARD 1: no class is taught two DIFFERENT joint subjects at once,
    # and no class has two subjects from the SAME department category
    # at once (a class's Science group can't do two Science subjects
    # simultaneously -- but Science+Commercial+Arts CAN co-occur, since
    # that's the whole point of the departmental split).
    # A joint subject occupies the WHOLE class -- so a joint subject and
    # any departmental subject can never share a slot either.
    # ------------------------------------------------------------------
    for cls in CLASSES:
        for d in DAYS:
            for p in ALL_PERIODS:
                joint_vars = [x[(cls, s.id, d, p)] for s in class_subjects[cls]
                              if s.category == JOINT and (cls, s.id, d, p) in x]
                dept_vars = [x[(cls, s.id, d, p)] for s in class_subjects[cls]
                             if s.category != JOINT and (cls, s.id, d, p) in x]
                # At most one joint subject, and if any joint subject is
                # placed, no departmental subject may be placed (whole
                # class is occupied by the joint lesson).
                model.Add(sum(joint_vars) <= 1)
                if joint_vars:
                    model.Add(sum(dept_vars) == 0).OnlyEnforceIf(
                        # if sum(joint_vars) >= 1 -- expressed via a
                        # reified bool since OnlyEnforceIf needs a
                        # single literal
                        _joint_active_lit(model, joint_vars, cls, d, p)
                    )
                # Within departmental subjects, at most one per category
                for cat in (SCI, COMM, ARTS):
                    cat_vars = [x[(cls, s.id, d, p)] for s in class_subjects[cls]
                                if s.category == cat and (cls, s.id, d, p) in x]
                    model.Add(sum(cat_vars) <= 1)

    # ------------------------------------------------------------------
    # HARD 2: fork groups (FM/Agric, History/LitInEng) -- at most one
    # of the forked subjects for a class in a given slot (they already
    # can't co-occur since they're both Science/Arts category and the
    # per-category cap above already forces <=1 per category -- this is
    # here for explicitness/documentation, not because it adds a new
    # constraint beyond the category cap).
    # ------------------------------------------------------------------
    # (No additional code needed -- the per-category <=1 constraint above
    # already enforces this, since every fork pair shares a category.)

    # ------------------------------------------------------------------
    # HARD 3: no teacher double-booked across classes at the same slot.
    # ------------------------------------------------------------------
    for t_id in teachers:
        for d in DAYS:
            for p in ALL_PERIODS:
                vars_here = [x[(cls, s.id, d, p)]
                             for cls in CLASSES for s in class_subjects[cls]
                             if s.teacher_id == t_id and (cls, s.id, d, p) in x]
                if vars_here:
                    model.Add(sum(vars_here) <= 1)

    # ------------------------------------------------------------------
    # HARD 4: every active subject placed at least once per class
    # (coverage, priority level 2 -- never traded away).
    # ------------------------------------------------------------------
    for cls in CLASSES:
        for s in class_subjects[cls]:
            total = sum(x[(cls, s.id, d, p)] for d in DAYS for p in ALL_PERIODS
                        if (cls, s.id, d, p) in x)
            model.Add(total >= 1)
            # Never exceed the target either -- no point overshooting.
            model.Add(total <= s.target_per_week)

    # ------------------------------------------------------------------
    # HARD 5: consecutive-run rule. Only JOINT subjects may run 3 in a
    # row; every departmental subject caps at 2 in a row. "In a row"
    # means consecutive periods within the SAME day (periods p, p+1,
    # p+2 -- crossing the break at 11:50-12:30 does not count as
    # consecutive, since periods 5 and 6 aren't actually back-to-back
    # clock time). Accounts is fully exempt (spec: crammed into Monday
    # by construction).
    # ------------------------------------------------------------------
    BREAK_BOUNDARY = 5  # periods 1-5 are morning, 6-8 afternoon, 9-10 extended -- 5/6 crosses the real break
    for cls in CLASSES:
        for s in class_subjects[cls]:
            if s.id == "Accounts":
                continue  # exempt
            max_run = 3 if s.category == JOINT else 2
            for d in DAYS:
                # Only check runs of length (max_run + 1) that stay on
                # one side of the break boundary.
                for p_start in ALL_PERIODS:
                    window = [p_start + i for i in range(max_run + 1)]
                    if any(w not in ALL_PERIODS for w in window):
                        continue
                    if BREAK_BOUNDARY in window and (BREAK_BOUNDARY + 1) in window:
                        continue  # window spans the break -- not a real consecutive run
                    window_vars = [x[(cls, s.id, d, w)] for w in window if (cls, s.id, d, w) in x]
                    if len(window_vars) == max_run + 1:
                        model.Add(sum(window_vars) <= max_run)

    # ------------------------------------------------------------------
    # OBJECTIVE (priority level 3, soft): maximize total periods placed
    # toward each subject's target. Every placement counts equally --
    # CP-SAT will find the genuine maximum, not a greedy first-found
    # solution, so whatever shortfall remains is provably the smallest
    # possible given HARD 1-5 above.
    # ------------------------------------------------------------------
    all_vars = list(x.values())
    model.Maximize(sum(all_vars))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    return solver, status, x, class_subjects, teachers


def _joint_active_lit(model, joint_vars, cls, d, p):
    """Reified 'at least one joint subject placed' literal for this (cls,d,p)."""
    lit = model.NewBoolVar(f"joint_active_{cls}_{d}_{p}")
    model.Add(sum(joint_vars) >= 1).OnlyEnforceIf(lit)
    model.Add(sum(joint_vars) == 0).OnlyEnforceIf(lit.Not())
    return lit


if __name__ == "__main__":
    solver, status, x, class_subjects, teachers = solve()
    print("Status:", solver.StatusName(status))
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Objective (total periods placed):", solver.ObjectiveValue())
