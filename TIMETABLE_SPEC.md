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

## Flagged — needs a direct answer, not a guess

**F1 — T12's Thursday availability.** The very last message of the
prior session said T12 (SS1's secondary DT teacher) "also won't be
available on Thursday morning" — but the session hit its message limit
immediately after, so it's unclear whether this was ever actually built
into a solve. Treating it as live unless told otherwise: **T12 = no
Thursday morning (periods 1–5), same shape as T3/T6.** Confirm?

**F2 — T13's real availability.** Never provided — every solve so far
has treated Lit-in-Eng as unrestricted, flagged explicitly as
provisional each time. This directly affects how much of History/Lit's
2+2 split is actually achievable. What are T13's actual constraints?

**F3 — SS1 Chemistry's real ceiling.** The 8/wk boost was the single
most contested number in the whole session — capacity math for it kept
being recomputed and kept coming up short (T1 needing 32–36 slots
against a 24–28-slot week). The session ended accepting real shortfalls
here more than once, without ever landing on one final number. Given
everything else now locked (T1 off Wed+Thu entirely, 2 of SS1's DT
periods moved to T12), what's the actual achievable ceiling — do you
want me to compute it fresh against this locked spec before promising
8/wk again, or set a lower, honestly-achievable target up front?

**F4 — Is Variant B still wanted?** The transcript carried two parallel
scenarios throughout — Variant A (T1 fully off Wed+Thu) and Variant B
(T1 off Wed+Thu for periods 1–8 but available for the 2:30–4:00
extended block both days). Do you still want both solved and compared
side by side, or has Variant A been decided as the real one to build?

**F5 — Genuine free periods vs. solver failure.** Once this spec is
confirmed, I'm treating **any blank cell in the final output as a bug
to fix, not an acceptable result** — the only free periods that should
exist are the honestly-reported, capacity-driven shortfalls listed
above (or discovered fresh once solving), each one named and explained
on the page itself, the way the better of the two existing files
already does it for its 8 free cells. Nothing should end up blank
just because a solver ran out of moves.

---

Once F1–F4 are answered, I'll rebuild the solver properly against this
locked spec and generate a clean output with zero unexplained blanks.
