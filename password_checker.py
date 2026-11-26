import re
import getpass
import math
import os

# The common-password list lives in its own file, next to this script
COMMON_PASSWORDS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "common_passwords.txt"
)

# Characters that count as "special"
SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.?/"

# Rough assumption: a fast attacker can try 10 billion guesses per second
GUESSES_PER_SECOND = 10_000_000_000


def load_common_passwords(filename=COMMON_PASSWORDS_FILE):
    """Read one password per line from a text file and return them as a set."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print("Warning: common_passwords.txt not found, so the common-password check is skipped.")
        return set()


def check_password_strength(password, common_passwords=()):
    """Return (level, feedback, score). The score goes from 0 to 6."""

    # A common password is weak no matter what else it contains
    if password.lower() in common_passwords:
        return "Weak", ["This is a very common password. Choose something unique."], 0

    strength = 0
    feedback = []

    # Length check (longer is better)
    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
        feedback.append(
            f"Add {12 - len(password)} more characters to reach 12 for a stronger password."
        )
    else:
        feedback.append(
            f"Add {8 - len(password)} more characters to reach the minimum of 8."
        )

    # Uppercase check
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Lowercase check
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Number check
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        feedback.append("Add at least one number.")

    # Special character check
    if any(ch in SPECIAL_CHARS for ch in password):
        strength += 1
    else:
        feedback.append("Add at least one special character.")

    # Strength classification
    if strength <= 2:
        level = "Weak"
    elif strength <= 4:
        level = "Medium"
    else:
        level = "Strong"

    return level, feedback, strength


def format_duration(seconds):
    """Turn a number of seconds into a short, readable phrase."""
    if seconds < 1:
        return "less than a second"
    if seconds < 60:
        return f"about {seconds:.0f} seconds"
    minutes = seconds / 60
    if minutes < 60:
        return f"about {minutes:.0f} minutes"
    hours = minutes / 60
    if hours < 24:
        return f"about {hours:.0f} hours"
    days = hours / 24
    if days < 365:
        return f"about {days:.0f} days"
    years = days / 365
    if years < 1_000_000:
        return f"about {years:,.0f} years"
    return "more than a million years"


def estimate_crack_time(password, common_passwords=()):
    """Rough estimate of how long a fast attacker might need to guess the password."""
    if not password:
        return "instant"
    if password.lower() in common_passwords:
        return "instant (it is on the common-password list)"

    # Size of the character pool, based on which character types are used
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if any(ch in SPECIAL_CHARS for ch in password):
        pool += len(SPECIAL_CHARS)

    # Guesses needed is pool ** length. Using logarithms avoids huge numbers.
    log_seconds = len(password) * math.log10(pool) - math.log10(GUESSES_PER_SECOND)
    if log_seconds > 15:  # more than about 100 million years
        return "more than a million years"
    return format_duration(10 ** log_seconds)


def main():
    print("🔐 Password Strength Checker")
    print("--------------------------------")
    print("Type 'quit' to exit.\n")

    common_passwords = load_common_passwords()

    while True:
        # getpass hides what you type (in some IDEs it may still show it)
        password = getpass.getpass("Enter a password: ")

        if password.lower() == "quit":
            print("Goodbye!")
            break

        level, feedback, score = check_password_strength(password, common_passwords)
        crack_time = estimate_crack_time(password, common_passwords)

        print("\n--- Password Analysis ---")
        print("Password Length:", len(password))
        print(f"Score: {score}/6")
        print("Strength Level:", level)
        print(f"Rough crack time estimate: {crack_time}")

        if feedback:
            print("\nRecommendations to improve password:")
            for tip in feedback:
                print("-", tip)
        else:
            print("\nExcellent! Your password follows strong security practices.")

        print()


# Only run the program when this file is started directly,
# not when another file imports it
if __name__ == "__main__":
    main()
