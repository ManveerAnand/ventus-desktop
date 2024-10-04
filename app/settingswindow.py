import tkinter as tk
from tkinter import ttk

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Store reference to the main application
        self.title("Settings")
        self.geometry("400x300")  # Set size for the settings window

        self.create_settings_widgets()

    def create_settings_widgets(self):
        # --- Concurrent Connections ---
        connections_frame = ttk.LabelFrame(self, text="Concurrent Connections")
        connections_frame.pack(pady=10, padx=20, fill="x")

        self.connections_var = tk.IntVar(value=self.parent.settings.concurrent_connections)
        connections_spinbox = ttk.Spinbox(
            connections_frame,
            from_=1,
            to=10,
            textvariable=self.connections_var,
            width=5
        )
        connections_spinbox.pack(side="left", padx=5)

        # --- Max File Size ---
        filesize_frame = ttk.LabelFrame(self, text="Max File Size (MB)")
        filesize_frame.pack(pady=10, padx=20, fill="x")

        self.filesize_var = tk.IntVar(value=self.parent.settings.max_file_size_mb)
        filesize_spinbox = ttk.Spinbox(
            filesize_frame,
            from_=1,
            to=10000,  # Allow up to 10GB
            textvariable=self.filesize_var,
            width=5
        )
        filesize_spinbox.pack(side="left", padx=5)

        # --- Bandwidth Limit ---
        bandwidth_frame = ttk.LabelFrame(self, text="Bandwidth Limit (KB/s) - 0 for No Limit")
        bandwidth_frame.pack(pady=10, padx=20, fill="x")

        self.bandwidth_var = tk.IntVar(value=self.parent.settings.bandwidth_limit)
        bandwidth_entry = ttk.Entry(bandwidth_frame, textvariable=self.bandwidth_var, width=6)
        bandwidth_entry.pack(side="left", padx=5)

        # --- Sync Schedule (Dropdown) ---
        schedule_frame = ttk.LabelFrame(self, text="Sync Schedule")
        schedule_frame.pack(pady=10, padx=20, fill="x")

        schedule_options = ["Hourly", "Daily", "Weekly"]
        self.schedule_var = tk.StringVar(value=self.parent.settings.sync_schedule)

        schedule_dropdown = ttk.OptionMenu(schedule_frame, self.schedule_var, *schedule_options)
        schedule_dropdown.pack(side="left", padx=5)

        # --- Save Button ---
        save_button = ttk.Button(self, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=20)

    def save_settings(self):
        self.parent.settings.concurrent_connections = self.connections_var.get()
        self.parent.settings.max_file_size_mb = self.filesize_var.get()
        self.parent.settings.bandwidth_limit = self.bandwidth_var.get()
        self.parent.settings.sync_schedule = self.schedule_var.get()

        # ... (Implement actual saving of settings to a file in your Settings class)
        print("Settings saved! (Not yet implemented)")
