SCOPE Runtime -- "The Other Half" (elimination logic actually wired)

This is the part that didn't make it into your last push. The
pyproject.toml fix is already live on main -- good, leave that alone.
This is just the runtime/models fix, generated fresh against your
CURRENT main so it applies cleanly.

FILES:
- scope_the_other_half.diff  <- git diff of scope_runtime/models.py and
                                 scope_runtime/runtime.py, apply with:
                                 git apply scope_the_other_half.diff
- models.py                  <- full fixed file if you'd rather just copy
- runtime.py                 <- full fixed file if you'd rather just copy
- patched_demo.py            <- new file, not a diff -- just copy it into
                                 the repo root, shows the fix actually
                                 eliminating something

TO INSTALL (diff, from repo root):
  git apply /path/to/scope_the_other_half.diff
  cp /path/to/patched_demo.py .

TO INSTALL (manual copy):
  cp models.py   scope_runtime/models.py
  cp runtime.py  scope_runtime/runtime.py
  cp patched_demo.py .

VERIFY:
  PYTHONPATH=. python3 patched_demo.py
  -> should end with "Candidates: 3 -> 1" and two named eliminations,
     not "3 -> 3, nothing eliminated."

  Your existing example_scope_run.py will keep showing 3 -> 3 after this
  -- that's correct, not a leftover bug. Its falsifiers were never given
  an executable `check`, so they're still descriptive-only by design.
  The fix makes that distinction real instead of silent: any falsifier
  without a `check` now gets explicitly logged as "SKIP (no executable
  check)" instead of pretending to have been applied.

WHAT CHANGED:

models.py
  Falsifier gained `check: Optional[Callable[[CandidateStructure], bool]]`
  and `is_executable()`. A falsifier is either wired to real code or it
  isn't, and now the runtime can tell the difference instead of treating
  every falsifier as equally "applied."

runtime.py
  - Old `_phase_pressure` only logged falsifier names. Old `_phase_prune`
    eliminated purely on `assumption_count() > 4`, with no connection to
    falsifiers at all -- which is why the shipped example (all candidates
    at exactly 4 assumptions) never eliminated anything.
  - New `_phase_pressure_and_prune` actually calls `falsifier.check(candidate)`
    for every executable falsifier against every surviving candidate, and
    eliminates on a real trigger with a real recorded reason.
  - `execute()` now loops Pressure/Prune/Measure until nothing more gets
    eliminated (matching the paper's own "while EliminativeWorkExists"
    pseudocode) instead of running each phase exactly once. This also
    lets DRE history actually accumulate within a single run.
  - Fixed a stale-read bug: the "Admissibility maintained - survival
    rate: X%" log line was reading a value that hadn't been set yet and
    always printed 0.0%. Now computed live.

STILL OPEN, NOT ADDRESSED HERE:
  - The 18 tests referencing undefined fixtures (sample_candidates,
    basic_scope_run, etc.) -- still no conftest.py anywhere. Needs your
    call on what those fixtures should actually contain.
  - DRE's window_size=5 means short runs that converge in 1-2 iterations
    (like the demo) will never reach enough history for drift detection.
    Real per-scenario tuning question, not something to default silently.
  - Any falsifier's `check` function is only as good as what you write --
    the two in patched_demo.py are keyword-matching demos, not real
    external-data checks. Wiring the mechanism doesn't validate the
    specific falsifiers built on top of it.
