import math
import tkinter as tk
from tkinter import messagebox
def complex_calculator():
    def calculate():
        try:
            real1 = float(entry_real1.get())
            imag1 = float(entry_imag1.get())
            real2 = float(entry_real2.get())
            imag2 = float(entry_imag2.get())
            operation = operation_var.get()
            if operation == "Add":
                result_real = real1 + real2
                result_imag = imag1 + imag2
            elif operation == "Subtract":
                result_real = real1 - real2
                result_imag = imag1 - imag2
            elif operation == "Multiply":
                result_real = real1 * real2 - imag1 * imag2
                result_imag = real1 * imag2 + imag1 * real2
            elif operation == "Divide":
                denominator = real2**2 + imag2**2
                if denominator == 0:
                    messagebox.showerror("Error", "Cannot divide by zero")
                    return
                result_real = (real1 * real2 + imag1 * imag2) / denominator
                result_imag = (imag1 * real2 - real1 * imag2) / denominator
            else:
                messagebox.showerror("Error", "Invalid operation")
                return
            label_result.config(text=f"Result: {result_real} + {result_imag}i")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    root = tk.Tk()
    root.title("Complex Number Calculator")
    tk.Label(root, text="First Complex Number").grid(row=0, column=0, columnspan=2)
    tk.Label(root, text="Real Part:").grid(row=1, column=0)
    entry_real1 = tk.Entry(root)
    entry_real1.grid(row=1, column=1)
    tk.Label(root, text="Imaginary Part:").grid(row=2, column=0)
    entry_imag1 = tk.Entry(root)
    entry_imag1.grid(row=2, column=1)
    tk.Label(root, text="Second Complex Number").grid(row=3, column=0, columnspan=2)
    tk.Label(root, text="Real Part:").grid(row=4, column=0)
    entry_real2 = tk.Entry(root)
    entry_real2.grid(row=4, column=1)
    tk.Label(root, text="Imaginary Part:").grid(row=5, column=0)
    entry_imag2 = tk.Entry(root)
    entry_imag2.grid(row=5, column=1)
    operation_var = tk.StringVar(root)
    operation_var.set("Add")
    tk.OptionMenu(root, operation_var, "Add", "Subtract", "Multiply", "Divide").grid(row=6, column=0, columnspan=2)
    tk.Button(root, text="Calculate", command=calculate).grid(row=7, column=0, columnspan=2)
    label_result = tk.Label(root, text="Result: ")
    label_result.grid(row=8, column=0, columnspan=2)
    root.mainloop()
if __name__ == "__main__":
    complex_calculator()