# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Fix the Game Glitch Investigator project: reproduce the bugs, move the game logic into `logic_utils.py`, fix it, add `pytest` tests, and update the README and reflection, committing in separate steps.

**What did the agent do?**

1. Read `app.py`, `logic_utils.py`, and the starter tests.
2. Ran the original functions directly in Python to reproduce bugs (for example `check_guess(9, "50")` returned "Too High") and ran `pytest` (3 failures, `NotImplementedError`).
3. Added `# FIXME` comments at each bug and filled in the Bug Reproduction Log. Commit 1.
4. Moved the four logic functions into `logic_utils.py`, fixed them, and updated `app.py` to import them, added a `start_new_game()` helper, and fixed the attempt counter. Commit 2.
5. Wrote 7 new tests and fixed the 3 starter tests to unpack `(outcome, message)`. Ran `pytest` (10 passed).
6. Used Streamlit's `AppTest` to play scripted games (win, invalid input, lose, New Game, change difficulty) and confirm there were no exceptions.
7. Updated `README.md` and `reflection.md`. Commit 3.

**What did you have to verify or fix manually?**

The starter tests were themselves wrong (they compared a tuple to a string), so they had to be changed, not just the code. I also checked that the Demo Walkthrough numbers (final score 70 after guesses 70, abc, 30, 41) match what the game actually prints, and that `pytest` works from the project root (an empty `conftest.py` was added for that).

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Secret stored as a string | Test that `check_guess` handles `"50"` like `50` | `check_guess(9, "50")` is "Too Low", `check_guess(100, "50")` is "Too High" | Yes | This was the actual bug on even attempts |
| Decimal input | Test `parse_guess` with decimals | `"10.0"` accepted as 10, `"12.7"` rejected | Yes | Silently truncating 12.7 to 12 would be confusing |
| Out-of-range input | Test `parse_guess` with range limits | `"0"` and `"101"` rejected for 1-100, `"100"` accepted | Yes | Checks both edges of an inclusive range |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
