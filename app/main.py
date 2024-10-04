import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import pyzbar.pyzbar as pyzbar
import threading
import time
from settings import Settings
from sync_engine import SyncEngine
from settingswindow import SettingsWindow


class ConnectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Connection Settings")
        self.connection_manager = parent.connection_manager

        self.create_connection_widgets()

    def create_connection_widgets(self):
        link_frame = ttk.Frame(self)
        link_frame.pack(pady=10)

        link_label = ttk.Label(link_frame, text="Connection String:")
        link_label.pack(side="left", padx=5)

        self.link_entry = ttk.Entry(link_frame, width=30)
        self.link_entry.pack(side="left", padx=5)

        connect_link_button = ttk.Button(link_frame, text="Connect", command=self.connect_via_link)
        connect_link_button.pack(side="left", padx=5)

    def connect_via_link(self):
        connection_string = self.link_entry.get()
        self.connection_manager.set_connection_status(True, connection_string)
        self.destroy()

class ConnectionManager:
    def __init__(self, app):
        self.app = app
        self.connection_string = None
        self.connected = False

    def connect(self):
        connection_window = ConnectionWindow(self.app)
        self.app.wait_window(connection_window)
        return self.connected

    def set_connection_status(self, status, connection_string=None):
        self.connected = status
        self.connection_string = connection_string

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FileSync App")
        self.geometry("600x400")

        self.settings = Settings()
        self.connection_manager = ConnectionManager(self)
        self.sync_engine = SyncEngine(self)
        self.sync_thread = None

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=6, relief="flat", background="#5cb85c")
        style.configure("TLabel", background="#f0f0f0")

        connection_frame = ttk.Frame(self)
        connection_frame.pack(pady=20)

        connect_button = ttk.Button(connection_frame, text="Connect", command=self.initiate_connection, width=15)
        connect_button.pack(side="left", padx=5)

        self.connection_label = ttk.Label(connection_frame, text="Not Connected", foreground="red")
        self.connection_label.pack(side="left", padx=5)

        settings_frame = ttk.Frame(self)
        settings_frame.pack(pady=10)

        settings_button = ttk.Button(settings_frame, text="Settings", command=self.open_settings, width=15)
        settings_button.pack()

        sync_frame = ttk.Frame(self)
        sync_frame.pack(pady=20)

        sync_button = ttk.Button(sync_frame, text="Start Sync", command=self.toggle_sync, width=15)
        sync_button.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=400, variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.status_label = ttk.Label(self, text="Ready", background="#f0f0f0")
        self.status_label.pack()

    def initiate_connection(self):
        if self.connection_manager.connect():
            self.connection_label.config(text="Connected", foreground="green")
        else:
            self.connection_label.config(text="Connection Failed", foreground="red")

    def open_settings(self):
        settings_window = SettingsWindow(self)

    def toggle_sync(self):
        if self.sync_thread is None or not self.sync_thread.is_alive():
            self.sync_thread = threading.Thread(target=self.sync_engine.start_sync)
            self.sync_thread.start()
        else:
            self.stop_sync()

    def stop_sync(self):
        if self.sync_thread:
            self.sync_engine.stop_sync()
            self.sync_thread.join()
            self.sync_thread = None
            self.status_label.config(text="Sync Stopped")

# Settings Window with Content

if __name__ == "__main__":
    app = Application()
    app.mainloop()

