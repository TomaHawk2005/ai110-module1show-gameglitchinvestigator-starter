# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** A Streamlit number-guessing game. The player picks a difficulty (Easy 1-20, Normal 1-100, Hard 1-200), gets a limited number of attempts, and uses "Too High" / "Too Low" hints to find the secret number. Faster wins earn more points and every wrong guess costs 5 points.
- [x] **Bugs found:**
  - Hint messages were backwards ("Too High" told you to "Go HIGHER").
  - On every even-numbered attempt the secret was turned into a string, so comparisons were alphabetical (`"9" > "50"`), giving wrong hints and making some correct guesses fail.
  - Attempts started at 1, so the game said "7 attempts left" on Normal before you guessed.
  - "New Game" ignored the difficulty range and never reset the status, score, or history, so after a loss you stayed stuck on "Game over".
  - The "Guess a number between 1 and 100" text ignored the difficulty.
  - Scoring: a wrong "Too High" guess on even attempts *added* 5 points, and a first-try win only gave 80.
  - Hard (1-50) was actually easier than Normal (1-100).
  - Invalid input (like `abc`) still used up an attempt, and decimals like `12.7` were silently truncated.
  - "Attempts left" lagged one guess behind because it was drawn before the guess was processed.
  - All starter tests failed with `NotImplementedError` because the logic had not been moved into `logic_utils.py`.
- [x] **Fixes applied:**
  - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and imported them in `app.py`.
  - `check_guess` always compares integers and returns the correct messages; removed the string-comparison fallback.
  - Added a single `start_new_game()` helper used on first load, on "New Game", and when difficulty changes.
  - Attempts start at 0 and only valid guesses count. `parse_guess` strips spaces, rejects non-whole numbers, and rejects out-of-range guesses.
  - Every wrong guess costs 5 points; a first-try win is worth 100 (minimum 10).
  - "Attempts left" is drawn with an `st.empty()` placeholder that is filled at the end of the script.
  - Added regression tests for each fix in `tests/test_game_logic.py`.

## 📸 Demo Walkthrough

Example game on **Normal** (range 1-100, 8 attempts). The secret (visible in "Developer Debug Info") is 41.

1. The game loads and shows "Guess a number between 1 and 100. Attempts left: 8". Score is 0.
2. User enters `70`. The game shows "📉 Go LOWER!" (outcome "Too High"). Attempts left: 7, score: -5.
3. User enters `abc`. The game shows "That is not a number." Attempts left stays at 7 and the score does not change.
4. User enters `30`. The game shows "📈 Go HIGHER!" (outcome "Too Low"). Attempts left: 6, score: -10.
5. User enters `41`. Balloons appear and the game shows "You won! The secret was 41. Final score: 70" (100 - 2×10 for the 3rd attempt = 80, minus the two 5-point penalties).
6. User clicks **Submit** again: the game says "You already won. Start a new game to play again."
7. User clicks **New Game 🔁**: attempts reset to 8, score resets to 0, and a new secret is picked in the current range.
8. User switches the sidebar to **Easy**: the text changes to "between 1 and 20", attempts left becomes 6, and a fresh secret in 1-20 is picked.
9. If the user runs out of attempts, the game shows "Out of attempts! The secret was N" and **New Game** starts a playable game again.

## 🧪 Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/claude/game
collected 10 items

tests/test_game_logic.py ..........                                      [100%]

============================== 10 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [x] **Advanced edge-case testing:** `test_parse_guess_edge_cases` covers empty input, `None`, extra spaces, letters, decimals (`10.0` accepted, `12.7` rejected), and out-of-range guesses. `test_string_secret_compares_as_number` covers the string-vs-int comparison.
- [x] **Agent workflow:** documented in `ai_interactions.md`.
