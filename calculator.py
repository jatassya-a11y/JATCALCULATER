import tkinter as tk
from tkinter import font

APP_NAME = "JatCalculater"
VERSION = "1.0.0"
AUTHOR = "Jat"

class JatCalculater:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.resizable(False, False)
        self.root.configure(bg="#0D0D0D")

        self.expression = ""
        self.result_var = tk.StringVar(value="0")
        self.expr_var = tk.StringVar(value="")
        self.just_evaled = False

        self._build_ui()

    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg="#0D0D0D", pady=10)
        title_frame.pack(fill="x", padx=20)

        tk.Label(
            title_frame, text=APP_NAME,
            font=("Courier New", 13, "bold"),
            fg="#FF6B00", bg="#0D0D0D"
        ).pack(side="left")

        tk.Label(
            title_frame, text=f"v{VERSION}",
            font=("Courier New", 9),
            fg="#555555", bg="#0D0D0D"
        ).pack(side="right", pady=4)

        # Display
        display_frame = tk.Frame(self.root, bg="#1A1A1A", pady=16, padx=20)
        display_frame.pack(fill="x", padx=16)

        tk.Label(
            display_frame, textvariable=self.expr_var,
            font=("Courier New", 11), fg="#555555", bg="#1A1A1A",
            anchor="e"
        ).pack(fill="x")

        tk.Label(
            display_frame, textvariable=self.result_var,
            font=("Courier New", 36, "bold"), fg="#FFFFFF", bg="#1A1A1A",
            anchor="e"
        ).pack(fill="x")

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0D0D0D", padx=16, pady=16)
        btn_frame.pack()

        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7",  "8",   "9", "×"],
            ["4",  "5",   "6", "−"],
            ["1",  "2",   "3", "+"],
            ["xʸ", "0",   ".", "="],
        ]

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                self._make_btn(btn_frame, label, r, c)

        # Footer
        tk.Label(
            self.root, text=f"Made by {AUTHOR}  •  Python + Tkinter",
            font=("Courier New", 8), fg="#333333", bg="#0D0D0D"
        ).pack(pady=(0, 10))

    def _make_btn(self, parent, label, row, col):
        if label in ("÷", "×", "−", "+", "xʸ"):
            bg, fg, hover = "#FF6B00", "#FFFFFF", "#E05A00"
        elif label == "=":
            bg, fg, hover = "#FFFFFF", "#0D0D0D", "#DDDDDD"
        elif label in ("AC", "+/-", "%"):
            bg, fg, hover = "#2A2A2A", "#FF6B00", "#3A3A3A"
        else:
            bg, fg, hover = "#1E1E1E", "#FFFFFF", "#2E2E2E"

        btn = tk.Button(
            parent, text=label,
            font=("Courier New", 16, "bold"),
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            width=4, height=2, bd=0, cursor="hand2", relief="flat",
            command=lambda l=label: self._on_click(l)
        )
        btn.grid(row=row, column=col, padx=5, pady=5)

    def _on_click(self, label):
        if label == "AC":
            self.expression = ""
            self.result_var.set("0")
            self.expr_var.set("")
            self.just_evaled = False

        elif label == "+/-":
            cur = self.result_var.get()
            if cur not in ("0", "Error"):
                new = cur[1:] if cur.startswith("-") else "-" + cur
                self.result_var.set(new)
                self.expression = new

        elif label == "%":
            try:
                val = float(self.result_var.get()) / 100
                self.result_var.set(self._fmt(val))
                self.expression = str(val)
            except:
                self.result_var.set("Error")

        elif label in ("÷", "×", "−", "+", "xʸ"):
            op_map = {"÷": "/", "×": "*", "−": "-", "+": "+", "xʸ": "**"}
            op = op_map[label]
            if self.just_evaled:
                self.expression = self.result_var.get()
                self.just_evaled = False
            self.expression += op
            self.expr_var.set(self.expression)
            self.result_var.set("0")

        elif label == "=":
            try:
                expr = self.expression
                self.expr_var.set(expr + " =")
                result = eval(expr)
                self.result_var.set(self._fmt(result))
                self.expression = str(result)
                self.just_evaled = True
            except ZeroDivisionError:
                self.result_var.set("÷0 Error")
                self.expression = ""
            except:
                self.result_var.set("Error")
                self.expression = ""

        elif label == ".":
            cur = self.result_var.get()
            if self.just_evaled:
                cur = "0"
                self.expression = ""
                self.just_evaled = False
            if "." not in cur:
                new = cur + "."
                self.result_var.set(new)
                self.expression += "."

        else:  # number
            cur = self.result_var.get()
            if self.just_evaled:
                cur = "0"
                self.expression = ""
                self.just_evaled = False
            new = label if cur == "0" else cur + label
            self.result_var.set(new)
            self.expression += label

    def _fmt(self, val):
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(round(val, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = JatCalculater(root)
    root.mainloop()
