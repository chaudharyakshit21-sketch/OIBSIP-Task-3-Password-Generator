"""Task 3 (Beginner) - Command-line Random Password Generator (uses random + string)."""
import random
import string


def ask_length():
    while True:
        raw = input("Password length (minimum 8): ").strip()
        if not raw.isdigit():
            print("Please enter a whole number.")
        elif int(raw) < 8:
            print("Length must be at least 8 characters.")
        else:
            return int(raw)


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please answer y or n.")


def ask_pools():
    options = [("uppercase letters", string.ascii_uppercase),
               ("lowercase letters", string.ascii_lowercase),
               ("numbers", string.digits),
               ("symbols", string.punctuation)]
    while True:
        pools = [chars for label, chars in options if ask_yes_no(f"Include {label}?")]
        if len(pools) >= 2:
            return pools
        print("Select at least 2 character types. Let's try again.\n")


def generate(length, pools):
    # one guaranteed character from each chosen type, then fill the rest
    password = [random.choice(p) for p in pools]
    everything = "".join(pools)
    password += [random.choice(everything) for _ in range(length - len(password))]
    random.shuffle(password)
    return "".join(password)


def main():
    print("=== Random Password Generator ===")
    while True:
        length = ask_length()
        pools = ask_pools()
        print("\nGenerated password:", generate(length, pools), "\n")
        if not ask_yes_no("Generate another password?"):
            break
    print("Goodbye!")


if __name__ == "__main__":
    main()
