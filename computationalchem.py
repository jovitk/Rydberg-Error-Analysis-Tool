import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np

# Set the appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChemistryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CHY1005: Computational Chemistry Lab Tool")
        self.geometry("550x600")

        # Create Tabview
        self.tabview = ctk.CTkTabview(self, width=500, height=550)
        self.tabview.pack(padx=20, pady=20)

        self.tabview.add("Rydberg Visualizer")
        self.tabview.add("Error Propagation")

        self.setup_rydberg_tab()
        self.setup_error_tab()

    # --- TAB 1: RYDBERG VISUALIZER ---
    def setup_rydberg_tab(self):
        tab = self.tabview.tab("Rydberg Visualizer")
        
        ctk.CTkLabel(tab, text="Hydrogen Emission Spectrum", font=("Arial", 22, "bold")).pack(pady=10)
        ctk.CTkLabel(tab, text="Enter quantum levels to find wavelength and series.", font=("Arial", 12)).pack(pady=5)
        
        self.n1_input = ctk.CTkEntry(tab, placeholder_text="Lower level n1 (e.g., 2)", width=200)
        self.n1_input.pack(pady=10)
        
        self.n2_input = ctk.CTkEntry(tab, placeholder_text="Upper level n2 (e.g., 3)", width=200)
        self.n2_input.pack(pady=10)
        
        self.ryd_result = ctk.CTkLabel(tab, text="Wavelength: -- nm", text_color="cyan", font=("Arial", 16))
        self.ryd_result.pack(pady=15)
        
        self.series_label = ctk.CTkLabel(tab, text="Series: --", font=("Arial", 13))
        self.series_label.pack(pady=5)
        
        ctk.CTkButton(tab, text="Analyze & Plot (if visible)", command=self.run_rydberg).pack(pady=20)

    def run_rydberg(self):
        R_H = 1.097373e7  # Rydberg Constant in m^-1
        try:
            n1 = int(self.n1_input.get())
            n2 = int(self.n2_input.get())
            
            if n2 <= n1:
                self.ryd_result.configure(text="Error: n2 must be > n1", text_color="red")
                return
            
            # Rydberg Formula: 1/λ = R_H * (1/n1² - 1/n2²)
            wavelength_m = 1 / (R_H * (1/(n1**2) - 1/(n2**2)))
            nm = wavelength_m * 1e9
            
            # Identify the scientific series
            series_map = {1: "Lyman (Ultraviolet)", 2: "Balmer (Visible)", 3: "Paschen (Infrared)", 
                          4: "Brackett (Infrared)", 5: "Pfund (Infrared)"}
            series_name = series_map.get(n1, "Unnamed High-Level Series")
            
            self.ryd_result.configure(text=f"Wavelength: {nm:.2f} nm", text_color="cyan")
            self.series_label.configure(text=f"Series: {series_name}")

            # Plotting Logic: Only if it's the Balmer Series (n1=2)
            if n1 == 2:
                self.show_spectrum_plot(nm)
            else:
                self.series_label.configure(text=f"Series: {series_name}\n(Invisible: No Plot Generated)")

        except ValueError:
            self.ryd_result.configure(text="Invalid Input", text_color="red")

    def show_spectrum_plot(self, wavelength_nm):
        plt.figure(figsize=(8, 3))
        plt.gca().set_facecolor('black')
        
        # Approximate color for the Balmer lines
        if wavelength_nm > 620: color = 'red'
        elif wavelength_nm > 590: color = 'orange'
        elif wavelength_nm > 490: color = 'cyan'
        else: color = 'blue'
        
        plt.axvline(x=wavelength_nm, color=color, lw=8, label=f"Target: {wavelength_nm:.1f}nm")
        
        # Setting the visible spectrum limits
        plt.xlim(380, 750)
        plt.title("Visible Hydrogen Emission (Balmer Series)")
        plt.xlabel("Wavelength (nm)")
        plt.yticks([])
        plt.legend()
        plt.tight_layout()
        plt.show()

    # --- TAB 2: ERROR PROPAGATION ---
    def setup_error_tab(self):
        tab = self.tabview.tab("Error Propagation")
        
        ctk.CTkLabel(tab, text="Uncertainty Calculator", font=("Arial", 22, "bold")).pack(pady=10)
        
        self.val_a = ctk.CTkEntry(tab, placeholder_text="Value A (e.g., 10.5)", width=250)
        self.val_a.pack(pady=5)
        self.err_a = ctk.CTkEntry(tab, placeholder_text="Uncertainty dA (e.g., 0.1)", width=250)
        self.err_a.pack(pady=5)
        
        self.op_menu = ctk.CTkOptionMenu(tab, values=["Add / Subtract (±)", "Multiply / Divide (×/÷)"], width=250)
        self.op_menu.pack(pady=15)
        
        self.val_b = ctk.CTkEntry(tab, placeholder_text="Value B", width=250)
        self.val_b.pack(pady=5)
        self.err_b = ctk.CTkEntry(tab, placeholder_text="Uncertainty dB", width=250)
        self.err_b.pack(pady=5)
        
        self.err_result = ctk.CTkLabel(tab, text="Result: --", text_color="yellow", font=("Arial", 18, "bold"))
        self.err_result.pack(pady=25)
        
        ctk.CTkButton(tab, text="Calculate Uncertainty", command=self.run_error, fg_color="green", hover_color="darkgreen").pack(pady=10)

    def run_error(self):
        try:
            a, da = float(self.val_a.get()), float(self.err_a.get())
            b, db = float(self.val_b.get()), float(self.err_b.get())
            op = self.op_menu.get()

            if "Add" in op:
                # Delta X = sqrt(dA^2 + dB^2)
                res = a + b
                err = np.sqrt(da**2 + db**2)
            else:
                # Delta X/X = sqrt((dA/A)^2 + (dB/B)^2)
                res = a * b
                err = res * np.sqrt((da/a)**2 + (db/b)**2)

            self.err_result.configure(text=f"Result: {res:.4f} ± {err:.4f}")
        except:
            self.err_result.configure(text="Invalid Numerical Input", text_color="red")

if __name__ == "__main__":
    app = ChemistryApp()
    app.mainloop()