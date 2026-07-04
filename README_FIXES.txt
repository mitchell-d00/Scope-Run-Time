SCOPE Runtime Fixes -- what's here and how to install

FILES:
- scope_runtime_fixes.diff   <- git diff, apply with `git apply` (preferred)
- models.py                  <- full fixed file, drop into scope_runtime/models.py
- runtime.py                 <- full fixed file, drop into scope_runtime/runtime.py
- pyproject.toml             <- full fixed file, drop into repo root
- patched_demo.py            <- new demo showing real elimination happening,
                                 drop into repo root

TO INSTALL (option A -- diff, cleanest):
  cd Scope-Run-Time
  git apply /path/to/scope_runtime_fixes.diff
  (new file patched_demo.py needs to be added separately -- git diff of a
  new untracked file doesn't include the add; just copy it in directly)
  cp /path/to/patched_demo.py .

TO INSTALL (option B -- just copy files over):
  cp models.py       Scope-Run-Time/scope_runtime/models.py
  cp runtime.py       Scope-Run-Time/scope_runtime/runtime.py
  cp pyproject.toml    Scope-Run-Time/pyproject.toml
  cp patched_demo.py   Scope-Run-Time/patched_demo.py

VERIFY:
  cd Scope-Run-Time
  PYTHONPATH=. python3 patched_demo.py
  -> should show 2 of 3 candidates eliminated with real reasons attached,
     not the original "3 -> 3, nothing eliminated" result.

WHAT CHANGED, IN ONE LINE EACH:

1. pyproject.toml
   Fixed a duplicate TOML table declaration ([tool.setuptools.packages.find]
   was declared twice, once implicitly via `packages = { find = {} }` and
   once explicitly). This was breaking `pip install .` and pytest's config
   discovery entirely.

2. models.py
   Falsifier gained a real `check: Optional[Callable]` field. Before, a
   Falsifier only had `test_method: str` (a human-readable description)
   and a `result: Optional[bool]` that nothing ever set. Now a falsifier
   can carry an actual executable predicate, and `is_executable()` tells
   you whether it's wired up or still descriptive-only.

3. runtime.py -- the real fix
   - Old `_phase_pressure` just logged falsifier names; it never touched
     `.result` or any candidate.
   - Old `_phase_prune` eliminated candidates purely on
     `assumption_count() > 4`, completely disconnected from falsifiers,
     constraints, or the domain. In the shipped example, all 3 candidates
     had exactly 4 assumptions, so nothing was ever eliminated.
   - New `_phase_pressure_and_prune` actually calls each falsifier's
     `.check(candidate)` and eliminates on a real trigger, with a real
     elimination reason and a real reference to which falsifier did it.
   - `execute()` now loops Pressure/Prune/Measure (matching the paper's
     own pseudocode: "while EliminativeWorkExists(...)") instead of
     running each phase exactly once. This also means DRE history can
     actually accumulate within a single run instead of being
     structurally stuck at "insufficient history" forever.
   - Fixed a stale-read bug in `_check_termination`: the "Admissibility
     maintained - survival rate: X%" log line was reading
     `self.result.survival_rate()` before `final_viable_candidates` had
     ever been set, so it always printed 0.0% regardless of the real
     outcome. Now computed directly from live candidate state.

KNOWN LIMITATIONS LEFT AS-IS (not silently patched):

- The two example falsifier checks in patched_demo.py
  (`gaming_resistance_check`, `unbounded_overhead_check`) are keyword
  matches against a candidate's own declared text, not checks against
  real outside data. They're real, executable code now -- but still a
  thin stand-in for what a genuine domain falsifier needs. Don't mistake
  "it runs" for "it's validated against reality."

- DRE's `window_size=5` default means short runs that converge in 1-2
  iterations (like the demo) will never accumulate enough history to
  trigger drift detection. The loop can now accumulate history in
  principle, but whether 5 is the right window for a given use case is
  a real parameter to tune per scenario, not something fixed here.

- The 18 tests in tests/test_scope_core.py that reference undefined
  fixtures (sample_candidates, basic_scope_run, etc.) are still broken --
  there's no conftest.py anywhere in the repo defining them. Not fixed
  here since it wasn't clear what those fixtures were supposed to
  contain; that needs your judgment call, not a guess from me.
