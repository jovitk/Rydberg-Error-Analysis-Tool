import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChemistryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CHY1005: Computational Chemistry Lab Tool")
        self.geometry("550x670") 

        self.tabview = ctk.CTkTabview(self, width=500, height=620)
        self.tabview.pack(padx=20, pady=20)
        self.tabview.add("Rydberg Visualizer")
        self.tabview.add("Error Propagation")

        self.setup_rydberg_tab()
        self.setup_error_tab()

    def setup_rydberg_tab(self):
        tab = self.tabview.tab("Rydberg Visualizer")
        ctk.CTkLabel(tab, text="Hydrogen Emission Spectrum", font=("Arial", 22, "bold")).pack(pady=10)
        self.n1_input = ctk.CTkEntry(tab, placeholder_text="Lower level n_final (e.g., 2)", width=250); self.n1_input.pack(pady=10)
        self.n2_input = ctk.CTkEntry(tab, placeholder_text="Upper level n_initial (e.g., 3)", width=250); self.n2_input.pack(pady=10)
        self.ryd_result = ctk.CTkLabel(tab, text="Wavelength: -- nm", text_color="cyan", font=("Arial", 16)); self.ryd_result.pack(pady=15)
        self.series_label = ctk.CTkLabel(tab, text="Series: --", font=("Arial", 13)); self.series_label.pack(pady=5)
        ctk.CTkButton(tab, text="Analyze & Plot", command=self.run_rydberg).pack(pady=20)

    def run_rydberg(self):
        R_H = 1.097373e7
        try:
            n1, n2 = int(self.n1_input.get()), int(self.n2_input.get())
            if n2 <= n1:
                self.ryd_result.configure(text="Error: n_initial > n_final", text_color="red")
                return
            nm = (1 / (R_H * (1/(n1**2) - 1/(n2**2)))) * 1e9
            series_map = {1: "Lyman (UV)", 2: "Balmer (Visible)", 3: "Paschen (IR)", 4: "Brackett (IR)", 5: "Pfund (IR)"}
            self.ryd_result.configure(text=f"Wavelength: {nm:.2f} nm", text_color="cyan")
            self.series_label.configure(text=f"Series: {series_map.get(n1, 'Other')}")
            if n1 == 2: self.show_plot(nm)
        except: self.ryd_result.configure(text="Invalid Input", text_color="red")

    def show_plot(self, wavelength_nm):
        plt.figure(figsize=(8, 3)); plt.gca().set_facecolor('black')
        color = 'red' if wavelength_nm > 620 else 'orange' if wavelength_nm > 590 else 'cyan' if wavelength_nm > 490 else 'blue'
        plt.axvline(x=wavelength_nm, color=color, lw=8, label=f"{wavelength_nm:.1f}nm")
        plt.xlim(380, 750); plt.xlabel("Wavelength (nm)"); plt.yticks([]); plt.legend(); plt.tight_layout(); plt.show()

    def setup_error_tab(self):
        tab = self.tabview.tab("Error Propagation")
        ctk.CTkLabel(tab, text="Uncertainty Calculator", font=("Arial", 22, "bold")).pack(pady=10)
        self.val_a = ctk.CTkEntry(tab, placeholder_text="Value A", width=250); self.val_a.pack(pady=5)
        self.err_a = ctk.CTkEntry(tab, placeholder_text="Uncertainty dA", width=250); self.err_a.pack(pady=5)
        self.op_menu = ctk.CTkOptionMenu(tab, values=["Addition (A+B)", "Subtraction (A-B)", "Multiplication (AxB)", "Division (A/B)"], width=250); self.op_menu.pack(pady=15)
        self.val_b = ctk.CTkEntry(tab, placeholder_text="Value B", width=250); self.val_b.pack(pady=5)
        self.err_b = ctk.CTkEntry(tab, placeholder_text="Uncertainty dB", width=250); self.err_b.pack(pady=5)
        
        self.err_result = ctk.CTkLabel(tab, text="Result: --", text_color="yellow", font=("Arial", 16, "bold")); self.err_result.pack(pady=10)
        self.rel_err_label = ctk.CTkLabel(tab, text="Relative Error: -- %", text_color="white", font=("Arial", 12)); self.rel_err_label.pack(pady=5)
        ctk.CTkButton(tab, text="Calculate", command=self.run_error, fg_color="green").pack(pady=10)

    def run_error(self):
        try:
            a, da, b, db = float(self.val_a.get()), float(self.err_a.get()), float(self.val_b.get()), float(self.err_b.get())
            op = self.op_menu.get()

            # PROFESSOR METHOD IMPLEMENTATION
            if "Addition" in op or "Subtraction" in op:
                res = (a + b) if "Addition" in op else (a - b)
                err = da + db  # Absolute errors add directly
                rel_err = (err / abs(res)) * 100 if res != 0 else 0

            else:
                res = (a * b) if "Multiplication" in op else (a / b)
                if "Division" in op and b == 0:
                    raise ZeroDivisionError

                rel_err_val = (da/a) + (db/b)  # Relative errors add directly
                err = abs(res) * rel_err_val
                rel_err = rel_err_val * 100

            self.err_result.configure(text=f"Result: {res:.4f} ± {err:.4f}")
            self.rel_err_label.configure(text=f"Relative Error: {rel_err:.2f}%")

        except ZeroDivisionError:
            self.err_result.configure(text="Error: Div by Zero", text_color="red")
        except:
            self.err_result.configure(text="Invalid Input", text_color="red")

if __name__ == "__main__":
    app = ChemistryApp(); app.mainloop()