import re
import getpass

# A small starter list. Real password checkers use much larger lists.
COMMON_PASSWORDS = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]

# Characters that count as "special"
SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.?/"


def check_password_strength(password):
    """Return (level, feedback, score). The score goes from 0 to 6."""

    # A common password is weak no matter what else it contains
    if password.lower() in COMMON_PASSWORDS:
        return "Weak", ["This is a very common password. Choose something unique."], 0

    strength = 0
    feedback = []

    # Length check (longer is better)
    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
        feedback.append("Use 12 or more characters for a stronger password.")
    else:
        feedback.append("Password should be at least 8 characters long.")

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


def main():
    print("🔐 Password Strength Checker")
    print("--------------------------------")
    print("Type 'quit' to exit.\n")

    while True:
        # getpass hides what you type (in some IDEs it may still show it)
        password = getpass.getpass("Enter a password: ")

        if password.lower() == "quit":
            print("Goodbye!")
            break

        level, feedback, score = check_password_strength(password)

        print("\n--- Password Analysis ---")
        print("Password Length:", len(password))
        print(f"Score: {score}/6")
        print("Strength Level:", level)

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
