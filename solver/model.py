"""
Data model for the SS1-SS3 timetable, built directly against
TIMETABLE_SPEC.md (the locked spec in the repo root). Nothing in here
should be guessed -- every constant traces to a specific line in that
file. If the spec changes, this file changes; the solver script
(solve.py) should never need spec knowledge hard-coded into it.
"""

from dataclasses import dataclass, field

CLASSES = ["SS1", "SS2", "SS3"]

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Periods 1-8 are the regular day (8:20-2:30, break 11:50-12:30).
# Periods 9-10 are the extended block (2:30-4:00), available only on
# specific days per teacher/subject -- see EXTENDED_AVAILABLE_DAYS and
# the whitelist below. "Thursday morning" (T3/T6/T12's restriction)
# means periods 1-5 specifically (5 periods before break, not 4 -- the
# prior session's transcript corrected this explicitly: 8:20-11:40 is
# 5 periods, then break 11:50-12:30, then 3 more periods to 2:30).
REGULAR_PERIODS = list(range(1, 9))
EXTENDED_PERIODS = [9, 10]
ALL_PERIODS = REGULAR_PERIODS + EXTENDED_PERIODS
THURSDAY_MORNING_PERIODS = {1, 2, 3, 4, 5}

# Only these subjects may ever sit in periods 9-10, and only on the
# days each subject's own teacher is available there (a subject on
# the whitelist is still bound by its teacher's normal availability --
# the whitelist narrows WHICH days/subjects can use the extended
# block, it doesn't grant anyone new days).
EXTENDED_WHITELIST = {
    "Chemistry", "Math", "English", "DT", "Livestock",
    "Government", "Commerce", "Physics", "Civic",
}

# Departmental category each subject belongs to. Joint subjects have
# no category (they're not part of the 3-way split). Consecutive-run
# rule and "standalone" privilege both key off this: only category=None
# (joint) subjects may run 3-in-a-row or be the sole subject present in
# a departmental slot.
JOINT = "joint"
SCI = "science"
COMM = "commercial"
ARTS = "arts"


@dataclass
class Teacher:
    id: str
    name: str
    # Set of (day, period) tuples this teacher is NEVER available for.
    # Built from each teacher's row in TIMETABLE_SPEC.md's availability
    # table, not guessed.
    unavailable: set = field(default_factory=set)
    extended_days: set = field(default_factory=set)  # days this teacher may use periods 9-10, if any


@dataclass
class Subject:
    id: str
    name: str
    teacher_id: str
    category: str  # JOINT, SCI, COMM, or ARTS
    target_per_week: int  # aspirational -- see priority order, frequency may drop
    # Fork group: subjects in the same fork never co-occur in the same
    # class+slot (student picks one). None if not forked.
    fork_group: str | None = None
    active: bool = True  # False = deferred (e.g. Lit-in-Eng, T13 unknown)


def build_teachers() -> dict[str, Teacher]:
    """Every teacher's availability, straight from TIMETABLE_SPEC.md's table."""
    t = {}

    def unavailable_thursday_morning():
        return {("Thu", p) for p in THURSDAY_MORNING_PERIODS}

    # T1: DT (most of it), Chemistry (SS1), FM (all 3). Mon/Tue/Fri
    # only -- off Wed AND Thu entirely, including the extended block.
    t["T1"] = Teacher(
        id="T1", name="T1",
        unavailable={(d, p) for d in ("Wed", "Thu") for p in ALL_PERIODS},
        extended_days={"Mon", "Tue"},
    )
    # T2: Civic, Government. No restriction.
    t["T2"] = Teacher(id="T2", name="T2")
    # T3: Biology. No Thursday morning (periods 1-5).
    t["T3"] = Teacher(id="T3", name="T3", unavailable=unavailable_thursday_morning())
    # T4: Math, Physics. No restriction. Whitelisted for extended block
    # (Math is whitelisted; Physics is whitelisted too) -- available
    # Mon/Tue like other unrestricted teachers using the extended block,
    # per spec ("Available Mon/Tue for most subjects on the whitelist").
    t["T4"] = Teacher(id="T4", name="T4", extended_days={"Mon", "Tue"})
    # T5: Accounts. Monday only, any period. Not on the extended
    # whitelist, and Accounts is a regular-day-only subject per every
    # prior session's build -- no extended_days.
    t["T5"] = Teacher(
        id="T5", name="T5",
        unavailable={(d, p) for d in DAYS if d != "Mon" for p in ALL_PERIODS},
    )
    # T6: Livestock, Agric. No Thursday morning. Livestock is
    # whitelisted and per spec gets Thursday extended relief too.
    t["T6"] = Teacher(
        id="T6", name="T6",
        unavailable=unavailable_thursday_morning(),
        extended_days={"Mon", "Tue", "Thu"},
    )
    # T7: Marketing, History. No restriction. History is confirmed
    # full-time/unrestricted per this session's resolution of F1-F4.
    t["T7"] = Teacher(id="T7", name="T7")
    # T8: CRS, Yoruba. No restriction.
    t["T8"] = Teacher(id="T8", name="T8")
    # T9: Economics, Commerce. No restriction. Commerce is whitelisted.
    t["T9"] = Teacher(id="T9", name="T9", extended_days={"Mon", "Tue"})
    # T10: English. Not Fridays. Whitelisted.
    t["T10"] = Teacher(
        id="T10", name="T10",
        unavailable={("Fri", p) for p in ALL_PERIODS},
        extended_days={"Mon", "Tue"},
    )
    # T11: Chemistry (SS2/SS3 only). Tue/Thu only.
    t["T11"] = Teacher(
        id="T11", name="T11",
        unavailable={(d, p) for d in DAYS if d not in ("Tue", "Thu") for p in ALL_PERIODS},
    )
    # T12: DT (2/wk of SS1 only). Corps member -- no Thursday morning,
    # same shape as T3/T6 (resolved F1 this session).
    t["T12"] = Teacher(id="T12", name="T12", unavailable=unavailable_thursday_morning())
    # T13: Lit-in-Eng. Availability still unknown (F2, unresolved) --
    # every subject this teacher owns is `active=False` in
    # build_subjects(), so this teacher's row is never actually used
    # by the solver. Left here for completeness/documentation only.
    t["T13"] = Teacher(id="T13", name="T13")

    return t


def build_subjects() -> list[Subject]:
    """
    Every subject, its target, its teacher, and its department
    category. Targets are aspirational (priority order: availability >
    coverage > frequency) -- the solver is not required to hit these
    exactly, only to never violate availability and to place every
    active subject at least once before maximizing toward these counts.
    """
    return [
        # Joint (whole class, one teacher, one period)
        Subject("Math", "Math", "T4", JOINT, 5),
        Subject("English", "English", "T10", JOINT, 5),
        Subject("Civic", "Civic", "T2", JOINT, 4),
        Subject("Livestock", "Livestock", "T6", JOINT, 4),
        # DT is split across three actual teaching assignments:
        #   - T1 teaches DT to SS2 and SS3 fully (4/wk each)
        #   - SS1's DT is split between T1 (2/wk) and T12 (2/wk)
        # Modeled as three subject rows, each scoped to specific
        # classes in subjects_for_class() below, all sharing the
        # display name "DT" so the output merges them visually.
        Subject("DT_ss23", "DT", "T1", JOINT, 4),       # SS2, SS3 only
        Subject("DT_ss1_t1", "DT", "T1", JOINT, 2),     # SS1 only, T1's 2/wk slice
        Subject("DT_ss1_t12", "DT", "T12", JOINT, 2),   # SS1 only, T12's 2/wk slice

        # Science department
        Subject("Chem_SS1", "Chemistry", "T1", SCI, 8),   # target aspirational, see F3 resolution
        Subject("Chem_SS23", "Chemistry", "T11", SCI, 3),
        Subject("Physics", "Physics", "T4", SCI, 4),
        Subject("Biology", "Biology", "T3", SCI, 4),
        Subject("FM", "Further-Maths", "T1", SCI, 4, fork_group="fm_agric"),
        Subject("Agric", "Agric", "T6", SCI, 4, fork_group="fm_agric"),

        # Commercial department
        Subject("Commerce", "Commerce", "T9", COMM, 4),
        Subject("Marketing", "Marketing", "T7", COMM, 4),
        Subject("Accounts", "Accounts", "T5", COMM, 2),
        Subject("Economics", "Economics", "T9", COMM, 4),

        # Arts department
        Subject("Government", "Government", "T2", ARTS, 4),
        Subject("History", "History", "T7", ARTS, 4, fork_group="history_lit"),
        Subject("LitInEng", "Lit-in-Eng", "T13", ARTS, 2, fork_group="history_lit", active=False),
        Subject("Yoruba", "Yoruba", "T8", ARTS, 4),
        Subject("CRS", "CRS", "T8", ARTS, 4),
    ]


# Subjects each class actually takes. Per TIMETABLE_SPEC.md, all three
# classes take the full joint + all three departments (departments are
# sub-groups WITHIN each class, not a per-class restriction) --
# confirmed in the prior session's resolved model ("3 classes total,
# departments are just subgroups inside each"). DT's split rows are
# scoped per class here since they don't apply uniformly.
def subjects_for_class(cls: str, subjects: list[Subject]) -> list[Subject]:
    out = []
    for s in subjects:
        if not s.active:
            continue
        if s.id == "DT_ss23" and cls == "SS1":
            continue  # SS1's DT is split across DT_ss1_t1 + DT_ss1_t12 instead
        if s.id in ("DT_ss1_t1", "DT_ss1_t12") and cls != "SS1":
            continue  # both SS1-only slices
        if s.id == "Chem_SS1" and cls != "SS1":
            continue
        if s.id == "Chem_SS23" and cls == "SS1":
            continue
        out.append(s)
    return out
