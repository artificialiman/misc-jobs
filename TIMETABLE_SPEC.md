# SS1–SS3 Timetable — Locked Spec (reconstructed from the prior session)

Written before touching a solver again. The last session lost a huge
amount of time re-solving against a spec that kept shifting mid-solve —
this exists so that doesn't happen twice. Everything under "Locked" is
stated plainly as final. Everything under "Flagged" needs a direct
answer before a real solve starts, because guessing wrong here means
redoing the solve, not just patching it.

## Structure

- 3 classes: SS1, SS2, SS3. Same teacher pool serves all three — no
  teacher may be double-booked across classes at the same period.
- Day: 8:20am–2:30pm regular (8 × 40-min periods), break 11:50–12:30.
- Extended block: 2:30–4:00pm (periods 9–10), available on specific
  days per teacher (see Availability), restricted to a subject
  whitelist (see below).
- Each class splits into 3 departments — Science, Commercial, Arts —
  for departmental subjects, and sits together for joint subjects.

## Joint subjects (whole class together, one teacher, one period)

Math (T4), English (T10), Civic (T2), Livestock (T6), DT (T1 for
SS2/SS3 and 2 of SS1's 4 weekly periods; T12 for the other 2 of SS1's
DT periods — see Flagged, T12's availability).

## Departmental subjects (class splits 3 ways, same clock-slot)

**Science:** Chemistry (T1 for SS1; T11 for SS2/SS3), Physics (T4),
Biology (T3), Further-Maths/Agric (T1/T6, forked — a student takes one
or the other, both taught in the same slot).

**Commercial:** Commerce (T9), Marketing (T7), Accounts (T5), Economics
(T9).

**Arts:** Government (T2), History/Lit-in-Eng (T7/T13, forked — same
pattern as FM/Agric), Yoruba (T8), CRS (T8).

## Teacher availability

| Teacher | Subjects | Availability |
|---|---|---|
| T1 | DT (most of it), Chemistry (SS1), FM (all 3) | Mon/Tue/Fri only — off Wed **and** Thu entirely, including the extended block |
| T2 | Civic, Government | No restriction |
| T3 | Biology | No Thursday morning (periods 1–5) |
| T4 | Math, Physics | No restriction |
| T5 | Accounts | Monday only, any period |
| T6 | Livestock, Agric | No Thursday morning (periods 1–5) |
| T7 | Marketing, History | No restriction |
| T8 | CRS, Yoruba | No restriction |
| T9 | Economics, Commerce | No restriction |
| T10 | English | Not Fridays |
| T11 | Chemistry (SS2/SS3 only) | Tue/Thu only |
| T12 | DT (2/wk of SS1 only) | See Flagged below |
| T13 | Lit-in-Eng | See Flagged below |

## Extended-block (2:30–4:00pm) rules

- Whitelist — only these subjects may ever sit in periods 9–10:
  Chemistry, Math, English, DT, Livestock, Government, Commerce,
  Physics, Civic.
- Available Mon/Tue for most subjects on the whitelist.
- Thursday extended is open too, but only for DT/Livestock/Math/English
  "relief" — T1 himself never uses the Thursday extended window, even
  though DT (his subject) can run there via another teacher.

## Weekly frequency targets

| Subject | Target | Notes |
|---|---|---|
| Math | 5/wk | Floor of 4/wk explicitly acceptable if 5 can't fit |
| English | 5/wk | Same floor; T10 off Fridays makes this the tightest general |
| Civic, DT, Livestock | 4/wk each | |
| Physics, Biology, Government, Commerce, Marketing, Economics, Yoruba, CRS | 4/wk each | No boost attempted |
| FM/Agric | 4/wk each | Forked, paired — same slot, no boost |
| Accounts | 2/wk | Monday-only, by construction |
| Chemistry (SS1) | 8/wk boosted | Highest-priority ask in the whole spec — see Flagged |
| Chemistry (SS2/SS3) | 3/wk each via T11 | The earlier plan to top this up to 5/wk via T1 in the extended block ("Chemistry_ext") was explicitly accepted as unachievable — 3/wk is the real target now |
| History / Lit-in-Eng | 2/wk each | Forked, shared slot, split evenly by default |

## Consecutive-run rule (applies everywhere)

- Max 2 consecutive periods of the same subject, for everyone.
- **Accounts is fully exempt** — it's crammed into one day by
  construction and needs to run more than 2 in a row to fit.
- The privilege of running **3** consecutive periods, or of being the
  *only* department represented in a departmental slot ("standalone"),
  belongs **only** to the 5 joint/general subjects — Math, English,
  Civic, Livestock, DT. Every departmental subject (Chemistry, Physics,
  Biology, FM/Agric, Commerce, Marketing, Accounts' exemption aside,
  Economics, Government, History/Lit, Yoruba, CRS) may never exceed 2
  in a row, and every departmental time-slot must have **at least 2 of
  the 3 categories (Sci/Comm/Arts) filled** — never just 1.
- This was stated most forcefully about Biology specifically, but the
  rule as given ("only generals can have that") reads as general, not
  Biology-specific — applying it to everyone, not just Biology, unless
  told otherwise.
- Math/English should be scheduled as **double (2-period) blocks where
  the weekly count doesn't divide cleanly into all-singles.**

---

## Resolved (previously flagged F1–F4)

- **T12 (SS1's secondary DT teacher):** no Thursday morning (periods
  1–5) — he's a corps member, same restriction shape as T3/T6.
- **T13 (Lit-in-Eng):** availability still genuinely unknown. Stays
  unscheduled/deferred — do not guess a day for him. History (T7,
  full-time/unrestricted) is scheduled normally; Lit-in-Eng is left
  out of the solve entirely until his real availability is known.
- **SS1 Chemistry's ceiling:** not a fixed target. Priority order
  (below) governs — Chemistry gets exactly as many periods as T1's
  real, fully-committed weekly schedule allows once every teacher's
  availability and every subject's coverage is satisfied first. If
  that number is less than 8/wk, that's the honest answer, reported
  plainly, not chased further by inventing new capacity fixes.
- **Variant:** A only (T1 fully off Wed+Thu, including the extended
  block). Variant B is dropped.

## Priority order (governs every trade-off in the solver)

1. **Teacher availability** — never violated, under any circumstance.
2. **Subject coverage** — every active subject gets placed somewhere
   at least once, before any subject is allowed to hit its full
   target frequency.
3. **Frequency targets** — the weekly counts in the table above are
   aspirational once 1 and 2 are satisfied. If something must give,
   it's frequency that drops, never a teacher's availability and never
   a subject's basic coverage.

## F5 — Genuine free periods vs. solver failure

Any blank cell in the final output must be an honestly-reported,
capacity-driven shortfall — never just a slot the solver gave up on.
Every remaining gap gets named and explained directly on the output
page itself, the same way the better of the two existing HTML files
already did for its 8 free cells.

---

All previously-flagged points are now resolved. Solver build proceeds
against this spec as locked.
