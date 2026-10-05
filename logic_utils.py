# FIX: Refactored all game logic out of app.py into this file (with Claude as an
# agent) so it can be unit tested without running Streamlit.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard used to be 1-50, which was easier than Normal (1-100).
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            as_float = float(raw)
            # FIX: "12.7" used to be silently truncated to 12. Only whole numbers count.
            if not as_float.is_integer():
                return False, None, "Please enter a whole number."
            value = int(as_float)
        else:
            value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    # FIX: out-of-range guesses used to be accepted and cost an attempt.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: The original version caught TypeError and fell back to comparing
    # strings ("9" > "50"). We removed that fallback and always compare ints;
    # app.py no longer turns the secret into a string.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    # FIX: messages were backwards ("Too High" told you to go HIGHER).
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1 for the first guess, 2 for the second, and so on.
    """
    if outcome == "Win":
        # FIX: was 100 - 10 * (attempt_number + 1), so a first-try win only gave 80.
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    # FIX: "Too High" used to ADD 5 points on even attempts. Every wrong guess
    # now costs the same 5 points.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
