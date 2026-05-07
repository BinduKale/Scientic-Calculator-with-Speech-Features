import tkinter as tk
from tkinter import messagebox
import math
from audio_helper import PlayAudio

ob = PlayAudio(voice='male', rate=4)

class Calculator:

    def __init__(self):
        self.window = tk.Tk() 
        self.window.title("Scientific Calculator")
        self.window.geometry("400x500")
        self.window.configure(bg="black")
        self.window.resizable(True, True)

        self.expression = ""
        self.history = []

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self.display = tk.Entry(
            self.window,
            textvariable=self.display_var,
            font=("Calibre", 24, "bold"),
            bd=10,
            justify="right",
            bg="white",
            fg="black",
            insertbackground="black",
            state="readonly",
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=20, ipady=15)

        history_btn = tk.Button(
            self.window,
            text="🕐",
            font=("Calibre", 12, "bold"),
            bg="white",
            fg="black",
            bd=0,
            relief="flat",
            command=self.show_history,
        )
        history_btn.place(in_=self.display, relx=0.02, rely=0.5, anchor="w")

        buttons = [
            ['AC', 'Del', '(', ')', 'π'],
            ['sin', 'cos', 'tan', 'log', '√'],
            ['%', 'x10³', 'ln', 'xʸ', 'eˣ'],
            ['7', '8', '9', '/', 'x²'],
            ['4', '5', '6', '*', 'x³'],
            ['1', '2', '3', '-', '1/x'],
            ['0', '00', '.', '+', '='],
        ]

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):

                if text == "=":
                    bg = "lightgray"
                    cmd = self.calculate

                elif text in ["AC", "Del"]:
                    bg = "turquoise"
                    cmd = lambda t=text: self.button_click(t)

                else:
                    bg = "lightgray"
                    cmd = lambda t=text: self.button_click(t)

                tk.Button(
                    self.window,
                    text=text,
                    font=("Calibre", 14, "bold"),
                    width=5,
                    height=2,
                    bg=bg,
                    fg="black",
                    command=cmd,
                ).grid(row=r + 1, column=c, sticky="nsew", padx=3, pady=3)

        for i in range(8):
            self.window.rowconfigure(i, weight=1)

        for i in range(5):
            self.window.columnconfigure(i, weight=1)

        self.window.bind("<Key>", self.key_press)
        self.window.bind("<Return>", lambda event: self.calculate())
        self.window.bind("<BackSpace>", lambda event: self.button_click("Del"))

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("History")
        history_window.geometry("300x400")
        history_window.configure(bg="black")

        label = tk.Label(
            history_window,
            text="History",
            bg="black",
            fg="white",
            font=("Calibre", 11, "bold"),
        )
        label.pack(pady=10)

        self.history_list = tk.Listbox(
            history_window,
            bg="black",
            fg="white",
            font=("Calibre", 11),
            width=30,
            height=15,
            cursor="hand2",
            selectbackground="blue",
            selectforeground="black",
        )
        self.history_list.pack(padx=10, pady=10, fill="both", expand=True)

        for item in self.history:
            self.history_list.insert(tk.END, item)

        self.history_list.bind(
            "<ButtonRelease-1>",
            lambda e: self.load_from_history(history_window),
        )

        clear_btn = tk.Button(
            history_window,
            text="Clear History",
            font=("Calibre", 12, "bold"),
            bg="red",
            fg="white",
            command=self.clear_history,
        )
        clear_btn.pack(pady=10)

    def load_from_history(self, history_window):
        selection = self.history_list.curselection()
        if not selection:
            return
        item = self.history_list.get(selection[0])
        if " = " in item:
            expression = item.split(" = ")[0].strip()
            self.expression = expression
            self.display_var.set(self.expression)
        history_window.destroy()
        self.history_list = None

    def clear_history(self):
        self.history.clear()
        if hasattr(self, "history_list") and self.history_list:
            self.history_list.delete(0, tk.END)

    def button_click(self, value):
        ob.speak(value)

        if value == "AC":
            self.expression = ""
            self.display_var.set("0")

        elif value == "Del":
            cursor_pos = self.display.index(tk.INSERT)
            if cursor_pos > 0:
                current_text = self.display_var.get()
                new_text = current_text[:cursor_pos-1] + current_text[cursor_pos:]
                self.expression = new_text
                self.display_var.set(new_text if new_text else "0")
                self.display.icursor(cursor_pos-1)

        elif value == "π":
            self.expression += str(math.pi)
            self.display_var.set(self.expression)

        elif value == "√":
            if self.expression:
                self.expression = f"math.sqrt({self.expression})"
            else:
                self.expression = "math.sqrt("
            self.display_var.set(self.expression)

        elif value == "x²":
            self.expression += "**2"
            self.display_var.set(self.expression)

        elif value == "x³":
            self.expression += "**3"
            self.display_var.set(self.expression)

        elif value == "1/x":
            try:
                result = 1 / float(eval(self.expression, {"__builtins__": None}, {"math": math}))
                self.expression = str(result)
                self.display_var.set(self.expression)
            except ZeroDivisionError:
                self.show_error("Cannot divide by zero")
            except Exception:
                self.show_error()

        elif value == "eˣ":
            if self.expression:
                self.expression = f"math.exp({self.expression})"
            else:
                self.expression = "math.exp("
            self.display_var.set(self.expression)

        elif value in ["sin", "cos", "tan"]:
            if self.expression:
                self.expression = f"math.{value}({self.expression})"
            else:
                self.expression = f"math.{value}("
            self.display_var.set(self.expression)

        elif value == "log":
            if self.expression:
                self.expression = f"math.log10({self.expression})"
            else:
                self.expression = "math.log10("
            self.display_var.set(self.expression)

        elif value == "ln":
            if self.expression:
                self.expression = f"math.log({self.expression})"
            else:
                self.expression = "math.log("
            self.display_var.set(self.expression)

        elif value == "xʸ":
            self.expression += "**"
            self.display_var.set(self.expression)

        elif value == "x10³":
            self.expression += "*1000"
            self.display_var.set(self.expression)

        elif value == "%":
            self.expression += "/100"
            self.display_var.set(self.expression)

        elif value == "00":
            self.expression += "00"
            self.display_var.set(self.expression)

        else:
            self.expression += value
            self.display_var.set(self.expression)

    def calculate(self):
        try:
            open_count = self.expression.count('(')
            close_count = self.expression.count(')')
            if open_count > close_count:
                self.expression += ')' * (open_count - close_count)

            result = eval(self.expression, {"__builtins__": None}, {"math": math})

            if isinstance(result, float):
                result = round(result, 10)

            history_item = f"{self.expression} = {result}"
            self.history.append(history_item)

            self.expression = str(result)
            self.display_var.set(self.expression)

            ob.speak('=')
            for char in str(result):
                ob.speak(char)

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")

        except Exception:
            self.show_error("Error")

    def show_error(self, msg="Error"):
        ob.speak(msg)
        self.display_var.set(msg)
        self.expression = ""

    def key_press(self, event):
        key = event.char
        if key in "0123456789.+-*/()%":
            self.button_click(key)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()