"""Task 3 (Advanced) - Password Generator GUI using the secrets module."""
import secrets
import string
import tkinter as tk
from collections import deque
from tkinter import messagebox, ttk

try:
    import pyperclip
except ImportError:  # falls back to the tkinter clipboard
    pyperclip = None

AMBIGUOUS = set("0O1lI|")


def build_pools(upper, lower, digits, symbols, exclude_ambiguous):
    pools = []
    for enabled, chars in ((upper, string.ascii_uppercase), (lower, string.ascii_lowercase),
                           (digits, string.digits), (symbols, string.punctuation)):
        if enabled:
            if exclude_ambiguous:
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)
    return pools


def generate_password(length, pools):
    """Cryptographically secure; guarantees at least one character from every selected type."""
    chars = [secrets.choice(p) for p in pools]
    everything = "".join(pools)
    chars += [secrets.choice(everything) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def strength(length, types):
    score = (length >= 8) + (length >= 12) + (length >= 16) + (types >= 3) + (types == 4)
    if score <= 2:
        return "Weak", 33, "#c62828"
    if score == 3:
        return "Medium", 66, "#ef6c00"
    return "Strong", 100, "#2e7d32"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Password Generator")
        self.geometry("480x560")
        self.history = deque(maxlen=5)  # kept in memory only, never written to disk
        self.length = tk.IntVar(value=16)
        self.vars = {name: tk.BooleanVar(value=True) for name in ("Uppercase", "Lowercase", "Numbers", "Symbols")}
        self.ambiguous = tk.BooleanVar(value=False)
        self.build_ui()

    def build_ui(self):
        frame = ttk.LabelFrame(self, text="Options", padding=12)
        frame.pack(fill="x", padx=12, pady=10)
        row = ttk.Frame(frame)
        row.pack(fill="x")
        ttk.Label(row, text="Length:").pack(side="left")
        tk.Spinbox(row, from_=8, to=64, textvariable=self.length, width=5).pack(side="left", padx=6)
        tk.Scale(frame, from_=8, to=64, orient="horizontal", variable=self.length, showvalue=False).pack(fill="x")
        for name, var in self.vars.items():
            ttk.Checkbutton(frame, text=name, variable=var).pack(anchor="w")
        ttk.Checkbutton(frame, text="Exclude ambiguous characters (0 O 1 l I |)",
                        variable=self.ambiguous).pack(anchor="w", pady=(6, 0))

        ttk.Button(self, text="Generate (auto-copies)", command=self.generate).pack(pady=6)
        self.output = ttk.Entry(self, font=("Consolas", 14), justify="center")
        self.output.pack(fill="x", padx=12, pady=6)

        self.strength_label = ttk.Label(self, text="Strength: -", font=("Segoe UI", 11, "bold"))
        self.strength_label.pack()
        self.bar = ttk.Progressbar(self, maximum=100, length=300)
        self.bar.pack(pady=4)
        self.status = ttk.Label(self, text="")
        self.status.pack()
        ttk.Button(self, text="Copy to Clipboard", command=self.copy).pack(pady=4)

        hist = ttk.LabelFrame(self, text="Last 5 passwords (this session only)", padding=8)
        hist.pack(fill="both", expand=True, padx=12, pady=10)
        self.listbox = tk.Listbox(hist, font=("Consolas", 11), height=5)
        self.listbox.pack(fill="both", expand=True)

    def generate(self):
        selected = [v.get() for v in self.vars.values()]
        if sum(selected) < 2:
            messagebox.showerror("Selection error", "Select at least 2 character types.")
            return
        length = self.length.get()
        if length < 8:
            messagebox.showerror("Length error", "Password length must be at least 8.")
            return
        pools = build_pools(*selected, self.ambiguous.get())
        password = generate_password(length, pools)
        self.output.delete(0, "end")
        self.output.insert(0, password)

        label, value, color = strength(length, sum(selected))
        self.strength_label.config(text=f"Strength: {label}", foreground=color)
        self.bar["value"] = value
        self.history.appendleft(password)
        self.listbox.delete(0, "end")
        for p in self.history:
            self.listbox.insert("end", p)
        self.copy()

    def copy(self):
        password = self.output.get()
        if not password:
            return
        try:
            if pyperclip:
                pyperclip.copy(password)
            else:
                self.clipboard_clear()
                self.clipboard_append(password)
            self.status.config(text="Copied to clipboard")
        except Exception:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.status.config(text="Copied using tkinter clipboard")


if __name__ == "__main__":
    App().mainloop()
