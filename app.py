import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import urllib.request
import urllib.error
import json
import os

# =====================================================================
# CONFIGURATION — Backend runs on same machine
# =====================================================================
TEAMMATE_IP = "127.0.0.1"
BACKEND_URL = f"http://{TEAMMATE_IP}:8000/generate"
DOWNLOAD_URL = f"http://{TEAMMATE_IP}:8000/download"

class AppleLevelDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Test Suite Studio")
        self.root.geometry("1150x750")
        self.root.configure(bg="#1E1E1E")

        # Color Palette
        self.bg_dark = "#1E1E1E"
        self.panel_bg = "#252525"
        self.card_bg = "#2D2D2D"
        self.accent_blue = "#0A84FF"
        self.accent_green = "#30D158"
        self.accent_orange = "#FF9F0A"
        self.text_main = "#FFFFFF"
        self.text_muted = "#A1A1A6"
        self.terminal_green = "#30D5C8"

        self.setup_styles()
        self.build_hardware_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.panel_bg,
                        foreground=self.text_muted,
                        padding=[20, 8],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", self.card_bg)],
                  foreground=[("selected", self.accent_blue)])

        style.configure("TPanedwindow", background=self.bg_dark)

    def build_hardware_layout(self):
        # --- Top Header ---
        header = tk.Frame(self.root, bg=self.panel_bg, height=55)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text="Suite Studio", font=("Segoe UI Light", 15, "bold"), fg=self.text_main, bg=self.panel_bg)
        title.pack(side=tk.LEFT, padx=25)

        version_badge = tk.Label(header, text="v1.0.0", font=("Segoe UI", 8), fg=self.accent_blue, bg="#1E1E1E", padx=6, pady=2)
        version_badge.pack(side=tk.LEFT, padx=(0, 20))

        # ── Member 3 label REMOVED from here ──────────────────────────

        # --- Main Container ---
        canvas = tk.Frame(self.root, bg=self.bg_dark)
        canvas.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # ── Left Card (Input) ──────────────────────────────────────────
        left_card = tk.Frame(canvas, bg=self.panel_bg, width=420)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        left_card.pack_propagate(False)

        tk.Label(left_card, text="Agile Requirement Context",
                 font=("Segoe UI", 11, "bold"), fg=self.text_main,
                 bg=self.panel_bg).pack(anchor=tk.W, padx=20, pady=(20, 2))

        tk.Label(left_card, text="Drop user stories below to extract test suites.",
                 font=("Segoe UI", 9), fg=self.text_muted,
                 bg=self.panel_bg).pack(anchor=tk.W, padx=20, pady=(0, 12))

        # Input Text Box
        self.input_text = tk.Text(left_card, wrap=tk.WORD, font=("Consolas", 10),
                                   bg=self.card_bg, fg="#F5F5F7", bd=0,
                                   highlightthickness=1, highlightbackground="#3A3A3C",
                                   padx=12, pady=12)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        default_prompt = "As a customer,\nI want to secure my checkout with an email OTP token,\nSo that hackers cannot intercept my financial transactions."
        self.input_text.insert(tk.END, default_prompt)

        # ── Button Section ─────────────────────────────────────────────
        btn_frame = tk.Frame(left_card, bg=self.panel_bg)
        btn_frame.pack(fill=tk.X, padx=20, pady=(10, 5))

        # Main Generate Button
        self.submit_btn = tk.Button(
            btn_frame,
            text="Compile Test Matrix ⚡",
            bg=self.accent_blue,
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            activebackground="#0071E3",
            activeforeground="#FFFFFF",
            bd=0,
            cursor="hand2",
            pady=10,
            command=self.trigger_generation
        )
        self.submit_btn.pack(fill=tk.X, pady=(0, 8))

        # Download Button
        self.download_btn = tk.Button(
            btn_frame,
            text="⬇  Download .feature File",
            bg=self.accent_green,
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            activebackground="#28A745",
            activeforeground="#FFFFFF",
            bd=0,
            cursor="hand2",
            pady=8,
            command=self.download_feature_file
        )
        self.download_btn.pack(fill=tk.X, pady=(0, 5))
        self.download_btn.config(state=tk.DISABLED)

        # ── Right Card (Output) ────────────────────────────────────────
        right_card = tk.Frame(canvas, bg=self.bg_dark)
        right_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(right_card)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_cases, self.copy_cases_btn = self.spawn_premium_pane("🔍  Test Cases")
        self.tab_criteria, self.copy_criteria_btn = self.spawn_premium_pane("📋  Acceptance Criteria")
        self.tab_gherkin, self.copy_gherkin_btn = self.spawn_premium_pane("🥒  Gherkin Specs")

    def spawn_premium_pane(self, tab_title):
        frame = tk.Frame(self.notebook, bg=self.card_bg)

        copy_btn = tk.Button(
            frame,
            text="📋  Copy to Clipboard",
            bg=self.accent_orange,
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            activebackground="#E08800",
            activeforeground="#FFFFFF",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5
        )
        copy_btn.pack(anchor=tk.NE, padx=10, pady=(8, 0))
        copy_btn.config(state=tk.DISABLED)

        txt = tk.Text(
            frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.card_bg,
            fg=self.terminal_green,
            bd=0,
            insertbackground="white",
            padx=15,
            pady=15,
            highlightthickness=1,
            highlightbackground="#3A3A3C"
        )
        txt.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(frame, text=tab_title)
        return txt, copy_btn

    def copy_to_clipboard(self, text_widget):
        content = text_widget.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Copied!", "Content copied to clipboard successfully.")
        else:
            messagebox.showwarning("Empty", "Nothing to copy yet. Generate first.")

    def download_feature_file(self):
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".feature",
                filetypes=[("Feature Files", "*.feature"), ("All Files", "*.*")],
                initialfile="test_cases.feature",
                title="Save Feature File"
            )

            if not save_path:
                return

            req = urllib.request.Request(DOWNLOAD_URL, method="GET")
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode("utf-8")

            with open(save_path, "w") as f:
                f.write(content)

            messagebox.showinfo(
                "Download Complete ✅",
                f"Feature file saved successfully to:\n{save_path}"
            )

        except urllib.error.URLError:
            messagebox.showerror(
                "Download Failed",
                "Could not reach backend.\nMake sure backend is running on port 8000."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{str(e)}")

    def trigger_generation(self):
        user_story_content = self.input_text.get("1.0", tk.END).strip()

        if not user_story_content:
            messagebox.showwarning("Input Missing", "Please enter a requirement scenario.")
            return

        for tab in [self.tab_cases, self.tab_criteria, self.tab_gherkin]:
            tab.delete("1.0", tk.END)
            tab.insert(tk.END, "⚙️ Connecting to AI backend...\n")
        self.root.update()

        payload = json.dumps({"story": user_story_content}).encode("utf-8")
        req = urllib.request.Request(
            BACKEND_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))

                self.tab_cases.delete("1.0", tk.END)
                self.tab_cases.insert(tk.END, "🎯 POSITIVE FUNCTIONAL FLOWS:\n\n")
                for tc in data.get("positive_test_cases", []):
                    self.tab_cases.insert(tk.END, f"  ✔ {tc}\n")

                self.tab_cases.insert(tk.END, "\n❌ NEGATIVE EXCEPTION FLOWS:\n\n")
                for tc in data.get("negative_test_cases", []):
                    self.tab_cases.insert(tk.END, f"  ✘ {tc}\n")

                self.tab_cases.insert(tk.END, "\n⚠️ BOUNDARY & EDGE CONDITIONS:\n\n")
                for tc in data.get("edge_test_cases", []):
                    self.tab_cases.insert(tk.END, f"  ♦ {tc}\n")

                self.tab_criteria.delete("1.0", tk.END)
                self.tab_criteria.insert(tk.END, "📋 CORE VERIFICATION CHECKLIST:\n\n")
                for ac in data.get("acceptance_criteria", []):
                    self.tab_criteria.insert(tk.END, f"  [ ] {ac}\n")

                self.tab_gherkin.delete("1.0", tk.END)
                gherkin_str = f"Feature: {data.get('feature_name', 'Generated Feature')}\n\n"
                for sc in data.get("gherkin_scenarios", []):
                    gherkin_str += f"  Scenario: {sc.get('title', '')}\n"
                    for step in sc.get("steps", []):
                        gherkin_str += f"    {step}\n"
                    gherkin_str += "\n"
                self.tab_gherkin.insert(tk.END, gherkin_str.strip())

                self.download_btn.config(state=tk.NORMAL)

                self.copy_cases_btn.config(
                    state=tk.NORMAL,
                    command=lambda: self.copy_to_clipboard(self.tab_cases)
                )
                self.copy_criteria_btn.config(
                    state=tk.NORMAL,
                    command=lambda: self.copy_to_clipboard(self.tab_criteria)
                )
                self.copy_gherkin_btn.config(
                    state=tk.NORMAL,
                    command=lambda: self.copy_to_clipboard(self.tab_gherkin)
                )

        except urllib.error.URLError:
            for tab in [self.tab_cases, self.tab_criteria, self.tab_gherkin]:
                tab.delete("1.0", tk.END)
            messagebox.showerror(
                "Backend Not Running",
                f"Could not connect to backend at:\n{BACKEND_URL}\n\n"
                "To fix:\n"
                "1. Open a new terminal\n"
                "2. Run: cd backend\n"
                "3. Run: python main.py\n"
                "4. Wait for 'Uvicorn running on port 8000'\n"
                "5. Then click Compile Test Matrix again"
            )

        except Exception as e:
            for tab in [self.tab_cases, self.tab_criteria, self.tab_gherkin]:
                tab.delete("1.0", tk.END)
                tab.insert(tk.END, f"❌ Error: {str(e)}\n")
            messagebox.showerror("Unexpected Error", f"Something went wrong:\n\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppleLevelDashboard(root)
    root.mainloop()