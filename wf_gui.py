import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import json
import syndicate_mods_lookup
import wf_calculations


class SyndicateModsAnalyzerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Warframe Augment Seller")
        self.root.geometry("900x600")

        # Initialize mods list with default syndicate mods
        self.mods_to_analyze = syndicate_mods_lookup.syndicate_mods
        self.mod_source = "Warframe Augment List (updated 5/24/2025)"

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Warframe Augment Seller", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)

        # File selection button
        self.load_file_btn = ttk.Button(control_frame, text="Load Mods from File", command=self.load_mods_from_file)
        self.load_file_btn.pack(side=tk.LEFT, padx=5)

        # Mod source label
        self.source_var = tk.StringVar(value=f"Source: {self.mod_source} ({len(self.mods_to_analyze)} mods)")
        source_label = ttk.Label(control_frame, textvariable=self.source_var)
        source_label.pack(side=tk.LEFT, padx=5)

        # Limit entry
        limit_label = ttk.Label(control_frame, text="mods to analyze (0 for all):")
        limit_label.pack(side=tk.LEFT, padx=5)

        self.limit_var = tk.StringVar(value="0")
        limit_entry = ttk.Entry(control_frame, textvariable=self.limit_var, width=5)
        limit_entry.pack(side=tk.LEFT, padx=5)

        # Analyze button
        self.analyze_btn = ttk.Button(control_frame, text="Analyze Mods", command=self.start_analysis)
        self.analyze_btn.pack(side=tk.LEFT, padx=10)

        # Save button
        self.save_btn = ttk.Button(control_frame, text="Save Results", command=self.save_results, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        progress_bar.pack(fill=tk.X, pady=10)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W, pady=5)

        # Create notebook for results
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Log tab
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Log")

        self.log_text = scrolledtext.ScrolledText(log_frame)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Results")

        # Create two panes for 48h and 90d results
        results_paned = ttk.PanedWindow(results_frame, orient=tk.HORIZONTAL)
        results_paned.pack(fill=tk.BOTH, expand=True)

        # 48h results
        frame_48h = ttk.LabelFrame(results_paned, text="48 Hour Optimal Mods")
        results_paned.add(frame_48h, weight=1)

        self.results_48h = scrolledtext.ScrolledText(frame_48h)
        self.results_48h.pack(fill=tk.BOTH, expand=True)

        # 90d results
        frame_90d = ttk.LabelFrame(results_paned, text="90 Day Optimal Mods")
        results_paned.add(frame_90d, weight=1)

        self.results_90d = scrolledtext.ScrolledText(frame_90d)
        self.results_90d.pack(fill=tk.BOTH, expand=True)

        # Graph tab
        self.graph_frame = ttk.Frame(notebook)
        notebook.add(self.graph_frame, text="Graphs")

    def load_mods_from_file(self):
        """Allow user to select a file to load mods from"""
        file_path = filedialog.askopenfilename(
            title="Select Mods File",
            filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            mods_list = self.extract_mods_from_file(file_path)
            if mods_list and len(mods_list) > 0:
                self.mods_to_analyze = mods_list
                file_name = file_path.split("/")[-1]
                self.mod_source = f"Custom File: {file_name}"
                self.source_var.set(f"Source: {self.mod_source} ({len(self.mods_to_analyze)} mods)")
                self.log(f"Loaded {len(mods_list)} mods from {file_name}")
            else:
                messagebox.showwarning("No Mods Found", "No valid mod names were found in the selected file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load mods from file: {str(e)}")

    def extract_mods_from_file(self, file_path):
        """Extract mod names from a file"""
        try:
            file_ext = file_path.split(".")[-1].lower()

            if file_ext == "json":
                # Attempt to parse as JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Handle different JSON structures
                    if isinstance(data, list):
                        # Direct list of mod names
                        mods_list = data
                    elif isinstance(data, dict):
                        # Check for known structure patterns
                        if "mods" in data:
                            mods_list = data["mods"]
                        elif "items" in data:
                            mods_list = data["items"]
                        else:
                            # Use all string values as potential mod names
                            mods_list = []
                            for key, value in data.items():
                                if isinstance(value, str):
                                    mods_list.append(value)
                                elif isinstance(key, str) and not isinstance(value, (dict, list)):
                                    mods_list.append(key)

                    # Process mod names to match API format
                    processed_mods = []
                    for mod in mods_list:
                        if isinstance(mod, str) and len(mod) > 3:
                            mod_name = mod.replace(' ', '_').replace('\'', '').replace('&', 'and').lower()
                            processed_mods.append(mod_name)

                    return processed_mods
            else:
                # Use the syndicate_mods_lookup module to extract mods from the file
                return syndicate_mods_lookup.extract_mods_from_file(file_path)

        except Exception as e:
            self.log(f"Error extracting mods from file: {str(e)}")
            return []

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_analysis(self):
        # Get limit
        try:
            limit = int(self.limit_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the limit")
            return

        # Clear previous results
        self.log_text.delete(1.0, tk.END)
        self.results_48h.delete(1.0, tk.END)
        self.results_90d.delete(1.0, tk.END)

        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Disable buttons during analysis
        self.analyze_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.load_file_btn.config(state=tk.DISABLED)

        # Reset progress
        self.progress_var.set(0)
        self.status_var.set("Starting analysis...")

        # Start analysis in a thread
        threading.Thread(target=self.run_analysis, args=(limit,), daemon=True).start()

    def run_analysis(self, limit):
        try:
            # Get mods list
            all_mods = self.mods_to_analyze

            # Apply limit if needed
            if limit > 0:
                test_mods = all_mods[:limit]
            else:
                test_mods = all_mods

            self.log(f"Analyzing {len(test_mods)} out of {len(all_mods)} mods...")

            # Run the analysis
            self.mod_stats, self.pareto_optimal = self.analyze_mods(test_mods)

            # Update the UI with results
            self.root.after(0, self.update_results)

        except Exception as e:
            self.log(f"Error during analysis: {str(e)}")
            self.root.after(0, lambda: self.status_var.set("Analysis failed"))
            self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.load_file_btn.config(state=tk.NORMAL))

    def update_results(self):
        # Update status
        self.status_var.set("Analysis complete")

        # Display 48h results
        self.results_48h.delete(1.0, tk.END)
        self.results_48h.insert(tk.END, f"Found {len(self.pareto_optimal['48h'])} Pareto optimal mods:\n\n")

        for mod_name in self.pareto_optimal['48h']:
            stats = self.mod_stats[mod_name]
            self.results_48h.insert(tk.END, f"Mod: {mod_name.replace('_', ' ')}\n")
            self.results_48h.insert(tk.END, f"  Average Price: {stats['avg_price_48h']:.2f} platinum\n")
            self.results_48h.insert(tk.END, f"  Total Volume: {stats['volume_48h']} trades\n")

            if stats['moving_avg_48h']:
                self.results_48h.insert(tk.END, f"  Moving Average: {stats['moving_avg_48h']:.2f}\n")
            else:
                self.results_48h.insert(tk.END, "  Moving Average: N/A\n")

            self.results_48h.insert(tk.END, "\n")

        # Display 90d results
        self.results_90d.delete(1.0, tk.END)
        self.results_90d.insert(tk.END, f"Found {len(self.pareto_optimal['90d'])} Pareto optimal mods:\n\n")

        for mod_name in self.pareto_optimal['90d']:
            stats = self.mod_stats[mod_name]
            self.results_90d.insert(tk.END, f"Mod: {mod_name.replace('_', ' ')}\n")
            self.results_90d.insert(tk.END, f"  Average Price: {stats['avg_price_90d']:.2f} platinum\n")
            self.results_90d.insert(tk.END, f"  Total Volume: {stats['volume_90d']} trades\n")

            if stats['moving_avg_90d']:
                self.results_90d.insert(tk.END, f"  Moving Average: {stats['moving_avg_90d']:.2f}\n")
            else:
                self.results_90d.insert(tk.END, "  Moving Average: N/A\n")

            self.results_90d.insert(tk.END, "\n")

        # Create and display graphs
        self.create_graphs()

        # Re-enable buttons
        self.analyze_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.load_file_btn.config(state=tk.NORMAL)

    def create_graphs(self):
        # Create figure with two subplots
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.tight_layout(pad=3)

        for i, timeframe in enumerate(['48h', '90d']):
            ax = axes[i]

            # Plot all mods
            x, y = [], []
            for mod_name, stats in self.mod_stats.items():
                if stats[f'avg_price_{timeframe}'] > 0 and stats[f'volume_{timeframe}'] > 0:
                    x.append(stats[f'volume_{timeframe}'])
                    y.append(stats[f'avg_price_{timeframe}'])

            ax.scatter(x, y, alpha=0.5, label='All Mods')

            # Highlight Pareto optimal mods
            pareto_x, pareto_y, pareto_names = [], [], []
            for mod_name in self.pareto_optimal[timeframe]:
                stats = self.mod_stats[mod_name]
                pareto_x.append(stats[f'volume_{timeframe}'])
                pareto_y.append(stats[f'avg_price_{timeframe}'])
                pareto_names.append(mod_name)

            ax.scatter(pareto_x, pareto_y, color='red', label='Pareto Optimal')

            # Label the Pareto optimal points
            for j, name in enumerate(pareto_names):
                ax.annotate(name.replace('_', ' '), (pareto_x[j], pareto_y[j]),
                            textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

            # Add a line connecting the Pareto optimal points
            if len(pareto_x) > 1:
                # Sort points by x-coordinate
                pareto_points = sorted(zip(pareto_x, pareto_y), key=lambda p: p[0])
                pareto_x_sorted, pareto_y_sorted = zip(*pareto_points)
                ax.plot(pareto_x_sorted, pareto_y_sorted, 'r--', label='Pareto Front')

            ax.set_title(f'Pareto Optimal Mods ({timeframe})')
            ax.set_xlabel('Trading Volume')
            ax.set_ylabel('Average Price (platinum)')
            ax.grid(True, alpha=0.3)
            ax.legend()

        # Embed the figure in the UI
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_results(self):
        try:
            # Convert any non-serializable values to strings
            serializable_stats = {}
            for mod, stats in self.mod_stats.items():
                serializable_stats[mod] = {
                    key: float(value) if isinstance(value, (int, float)) else str(value)
                    for key, value in stats.items()
                }

            # Prepare data to save
            save_data = {
                'mod_stats': serializable_stats,
                'pareto_optimal_48h': self.pareto_optimal['48h'],
                'pareto_optimal_90d': self.pareto_optimal['90d'],
                'source': self.mod_source,
                'analysis_date': time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save to JSON
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")],
                title="Save Analysis Results"
            )

            if not file_path:
                return

            with open(file_path, 'w') as f:
                json.dump(save_data, f, indent=2)

            self.log(f"Results saved to {file_path}")
            messagebox.showinfo("Success", f"Results saved to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

        # This should be at the same indentation level as other methods in the class
    def analyze_mods(self, syndicate_mods):
        mod_stats = {}
        total_mods = len(syndicate_mods)

        self.log("Collecting statistics for mods...")

        # Iterate through the mods
        for i, mod_name in enumerate(syndicate_mods):
            # Update progress
            progress = (i / total_mods) * 100
            self.root.after(0, lambda p=progress: self.progress_var.set(p))
            self.root.after(0, lambda n=mod_name, c=i + 1, t=total_mods:
            self.status_var.set(f"Processing {c}/{t}: {n}"))

            if i % 5 == 0:
                self.log(f"Processing mod {i + 1}/{total_mods}: {mod_name}")



            # Get statistics for the mod
            stats = wf_calculations.get_mod_statistics(mod_name)
            if not stats:
                self.log(f"  Warning: Could not fetch statistics for {mod_name}")
                continue

            # Calculate averages for 48h and 90d
            avg_price_48h, volume_48h, moving_avg_48h = wf_calculations.calculate_averages(stats.closed_48h)
            avg_price_90d, volume_90d, moving_avg_90d = wf_calculations.calculate_averages(stats.closed_90d)

            mod_stats[mod_name] = {
                'avg_price_48h': avg_price_48h,
                'volume_48h': volume_48h,
                'moving_avg_48h': moving_avg_48h,
                'avg_price_90d': avg_price_90d,
                'volume_90d': volume_90d,
                'moving_avg_90d': moving_avg_90d
            }



            # Delay to avoid rate limiting
            time.sleep(0.1)

        # Find Pareto optimal mods
        pareto_optimal = wf_calculations.find_pareto_optimal_mods(mod_stats)

        # Update progress to 100%
        self.root.after(0, lambda: self.progress_var.set(100))

        self.log(f"Finished Processing: Click Results or Graphs Tab")

        return mod_stats, pareto_optimal

# This should be outside the class, at the root level of your script
if __name__ == "__main__":
    root = tk.Tk()
    app = SyndicateModsAnalyzerUI(root)
    root.mainloop()