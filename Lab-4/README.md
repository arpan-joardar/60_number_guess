# Lab 4 – VibeCoding: Number Guessing Repair Lab

Submitted by **Arpan Joardar** ([@arpan-joardar](https://github.com/arpan-joardar))

Assigned repo: [SETAPESU26/60_number_guess](https://github.com/SETAPESU26/60_number_guess)

## Contents

| Path | Description |
| --- | --- |
| [`videos/before_changes.mp4`](videos/before_changes.mp4) | Original game: two guesses, then submitting an empty box crashes it with `ValueError` (10 s) |
| [`videos/after_changes.mp4`](videos/after_changes.mp4) | Updated game: empty-submit warning, narrowing range, guess history, 7-attempt limit with Game Over, restart and a win (17 s) |
| [`code/`](code/) | Updated source code (same as the repository root) |

## What was changed

### Task 1 – Empty input crash (bug fix)

`submit_guess()` called `int()` on the raw text box value, so pressing Enter (or SUBMIT) with an
empty box raised `ValueError: invalid literal for int() with base 10: ''` and closed the game.
The input is now validated before it is parsed:

- empty submit → *"Please enter a number first!"* warning, no attempt used
- a number outside 1–100 → out-of-range warning, no attempt used
- the text box only accepts the digits 0–9, up to 3 characters

Also fixed: clicking SUBMIT no longer takes the focus away from the text box, and the keypad
Enter key submits too.

### Task 2 – Dynamic search range display

Every TOO LOW / TOO HIGH answer tightens a tracked lower/upper bound. The current window is shown
as `Range: low - high` together with a bar over the 1–100 number line that highlights the numbers
that are still possible.

### Task 3 – Recent guess history tracker

A panel on the right lists the last 7 guesses, newest first, with the attempt number and a
color-coded indicator: red ▲ **TOO HIGH**, blue ▼ **TOO LOW**, green ● **CORRECT**.
Empty or invalid submissions are not recorded.

### Task 4 – Maximum attempts & Game Over

Each round allows 7 attempts, which is always enough to find a number in 1–100 by halving the
range. The counter shows `Attempts: n / 7` and turns red when 2 or fewer are left. Missing on the
7th attempt shows a **Game Over** screen that reveals the hidden number. Press **R** to start a
new round after a win or a loss.

## Running

```bash
pip install pygame
python main.py
```

Works from the repository root or from `Lab-4/code/`.

**Controls:** type a number and press Enter (or click SUBMIT) to guess. Press R to start a new
round once the current one is over.
