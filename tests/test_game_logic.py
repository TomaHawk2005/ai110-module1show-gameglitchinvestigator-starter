from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# check_guess returns (outcome, message), so the starter tests now unpack the outcome.


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests for the bugs we fixed ---

def test_too_high_message_says_go_lower():
    # Bug: "Too High" used to tell the player to go HIGHER.
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


def test_string_secret_compares_as_number():
    # Bug: on even attempts the secret became a string, so "9" > "50" was True.
    outcome, _ = check_guess(9, "50")
    assert outcome == "Too Low"
    outcome, _ = check_guess(100, "50")
    assert outcome == "Too High"


def test_wrong_guess_never_adds_points():
    # Bug: "Too High" on an even attempt used to ADD 5 points.
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
    assert update_score(0, "Too Low", 2) == -5


def test_first_try_win_gives_full_points():
    # Bug: a first-try win used to give 80 instead of 100.
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 20) == 10  # never drops below 10


def test_hard_is_harder_than_normal():
    # Bug: Hard (1-50) used to be a smaller range than Normal (1-100).
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_parse_guess_edge_cases():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("  7  ") == (True, 7, None)
    assert parse_guess("10.0") == (True, 10, None)
    assert parse_guess("")[0] is False
    assert parse_guess(None)[0] is False
    assert parse_guess("abc")[0] is False
    assert parse_guess("12.7")[0] is False
    assert parse_guess("0", 1, 100)[0] is False
    assert parse_guess("101", 1, 100)[0] is False
    assert parse_guess("100", 1, 100) == (True, 100, None)
