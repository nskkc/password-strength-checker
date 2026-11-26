# 🔐 Password Strength Checker (Python)

## Overview
A beginner-friendly command-line tool that checks how strong a password is.
It scores the password against common password guidelines and gives tips to improve it.

## Features
- Length check (8+ characters, 12+ is better)
- Uppercase and lowercase letter detection
- Number detection
- Special character detection
- Common password detection (the list is in `common_passwords.txt`, so you can add more words without changing the code)
- Score out of 6 and a strength level (Weak / Medium / Strong)
- Rough crack time estimate (a guess based on how many characters are possible)
- Suggestions that say exactly how many characters to add
- Passwords are hidden while you type
- Check as many passwords as you want until you type `quit`

## How the Score Works

| Rule | Points |
|------|--------|
| 12+ characters | 2 |
| 8–11 characters | 1 |
| Uppercase letter | 1 |
| Lowercase letter | 1 |
| Number | 1 |
| Special character | 1 |

Levels: **Weak** (0–2), **Medium** (3–4), **Strong** (5–6).
A password on the common list is always **Weak**.

## Technologies Used
- Python 3
- Regular Expressions (`re` module)
- `getpass` module (hides password input)

No extra packages to install.

## How to Run
```bash
python3 password_checker.py
```

Keep `common_passwords.txt` in the same folder as `password_checker.py`.

Type a password and press Enter. Type `quit` to exit.

The crack time is a rough estimate. It assumes an attacker can try 10 billion guesses per second, which is a fast attacker, not a real-world measurement.


