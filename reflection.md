# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game it looked finished: a title, a difficulty picker, a text box, and Submit / New Game buttons. Playing it with the Developer Debug Info open showed it was broken. The hints were backwards (a guess above the secret said "Go HIGHER"), and on every second guess the hints flipped in confusing ways because the secret was being compared as a string. The game also said I had 7 attempts left on Normal before I had guessed anything, and after losing, "New Game" left me stuck on "Game over". Running `pytest` on the starter code failed all 3 tests with `NotImplementedError`.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60`, secret `50` | "Too High" with a hint to go **lower** | Outcome "Too High" but message says "📈 Go HIGHER!" (hint is backwards) | No error. `check_guess(60, 50)` returns `('Too High', '📈 Go HIGHER!')` |
| Guess `9` on an even-numbered attempt, secret `50` | "Too Low" | "Too High". On even attempts `app.py` turns the secret into a string, and `"9" > "50"` alphabetically | No error. `check_guess(9, "50")` returns `('Too High', ...)` |
| Guess `100` on an even-numbered attempt, secret `50` | "Too High" | "Too Low" (`"100" < "50"` as strings) | No error. `check_guess(100, "50")` returns `('Too Low', ...)` |
| Fresh game on Normal (8 attempts) | "Attempts left: 8" | "Attempts left: 7" because `attempts` starts at 1 | No error |
| Lose a game, then click **New Game** | Fresh, playable game | Still shows "Game over" because `status` is never reset; secret is always 1-100 even on Easy | No error |
| Wrong guess that is "Too High" on attempt 2 | Score goes down | Score goes **up** by 5 (`update_score(0, "Too High", 2)` returns `5`) | No error |
| Run `pytest` on the starter code | Tests run | All 3 tests fail | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**Tools:** I used Claude (in the Claude desktop app) as an agent. It read the starter files, ran the original functions directly to reproduce the bugs, did the refactor into `logic_utils.py`, wrote the tests, and ran both `pytest` and Streamlit's `AppTest` to check the game end to end. I reviewed the diffs and the test results.

**A correct AI suggestion:** Claude pointed out that "Attempts left" was always one guess behind, because `st.info(...)` is drawn near the top of `app.py` while the attempt counter is only updated further down, after Submit is handled. It suggested reserving the spot with `info_box = st.empty()` and filling it in at the end of the script. This was correct because Streamlit draws widgets in the order the script runs, so the box now uses the updated count. I verified it with an `AppTest` run: after the first guess the box read "Attempts left: 7" instead of 8.

**A suggestion I did not accept as written:** The original AI-generated `check_guess` had a `try/except TypeError` block that, when the secret was a string, converted the guess to a string and compared the two as text. That was the AI's own "fix" for a type mismatch it created itself. Patching that fallback would have kept a hidden bug around (`"9" > "50"` is `True`), so we removed it entirely, made `check_guess` convert both values to `int`, and stopped `app.py` from turning the secret into a string. I verified it with `test_string_secret_compares_as_number`, which checks that `check_guess(9, "50")` is "Too Low" and `check_guess(100, "50")` is "Too High".

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed only when two things were true: a `pytest` test that targets that exact bug passed, and the live game behaved correctly. For example, `test_too_high_message_says_go_lower` checks that a guess of 60 against a secret of 50 gives "Too High" with a "LOWER" message, and `test_wrong_guess_never_adds_points` checks that `update_score(0, "Too High", 2)` is now -5 (the original returned +5). The starter tests also had a bug of their own: they compared the whole `(outcome, message)` tuple to a string like `"Win"`, so they were updated to unpack the outcome first. AI helped write the edge-case tests for `parse_guess` (spaces, `None`, letters, `10.0` vs `12.7`, out-of-range guesses), and all 10 tests pass. I also used Streamlit's `AppTest` to play a scripted game (70 → abc → 30 → 41) and confirmed the hints, attempts left, and final score of 70 match the Demo Walkthrough in the README.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type in a box, Streamlit runs your whole Python script again from top to bottom. That is a "rerun". Normal variables get recreated each time, so anything the game needs to remember between clicks (the secret number, attempts, score, history) has to live in `st.session_state`, which is like a dictionary that survives reruns. Because the script runs in order, something drawn near the top of the page shows values from *before* the button click is handled lower down, which is exactly why "Attempts left" lagged by one. Resetting the game means resetting every value in session state, not just one or two, which is what the original "New Game" button got wrong.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

- **Habit to keep:** Writing one small `pytest` test for each bug, named after the bug, before calling it fixed. It turns "I think it works" into proof, and it will catch the bug if it ever comes back.
- **Do differently:** Give the AI one bug at a time and read every diff more slowly. Letting an agent fix many things in one pass is fast, but it makes it harder to tell which change fixed which problem.
- **How my thinking changed:** AI-generated code can look clean and "production-ready" while hiding logic bugs, and sometimes the AI's own error handling (like the `TypeError` fallback) is what hides them, so tests and human review are what make AI code trustworthy.
