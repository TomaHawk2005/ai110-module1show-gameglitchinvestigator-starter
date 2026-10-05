# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

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

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
