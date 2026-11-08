# Task 3 - Random Password Generator (Python)

- `password_beginner.py` - CLI using `random` and `string`; min length 8, at least 2 character types, generate-again loop.
- `password_advanced.py` - tkinter GUI using `secrets`, with:
  - length spinbox + slider, character-type checkboxes
  - guaranteed at least one character from each selected type
  - strength indicator (Weak / Medium / Strong) from length and diversity
  - auto-copy on generation via `pyperclip` (falls back to the tkinter clipboard)
  - option to exclude ambiguous characters (0 O 1 l I |)
  - last 5 passwords shown for the session only

## Setup & run
```
pip install -r requirements.txt
python password_beginner.py
python password_advanced.py
```
## Security notes
- The advanced version uses `secrets` (cryptographically secure). `random` in the beginner version is **not** suitable for real passwords.
- History is held in memory only and is never saved to a file.
- Copying to the clipboard exposes the password to other apps that read it; clear your clipboard afterwards.
