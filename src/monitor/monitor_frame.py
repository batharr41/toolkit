import customtkinter as ctk
import psutil
import threading
from orginizer.tools_header import ToolsHeader
from snapshots import SnapshotsFrame
from . import processes_frame

# Set up appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")


class MonitorFrame(ctk.CTkFrame):
    """
    A customtkinter application to display live CPU and RAM usage
    for top system processes using the psutil library.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- 1. Title ---
        self.header = ToolsHeader(self, "monitor.png", "System Monitor")
        self.header.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="n")

        # --- 2. Snapshots ---
        self.snapshots = SnapshotsFrame(self)
        self.snapshots.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # --- 3. Processes ---
        self.processes = processes_frame.ProcessesFrame(self)
        self.processes.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ewns")


class MonitorWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("System Monitor")
        self.geometry("550x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = MonitorFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("System Monitor App")
    app.geometry("400x700")

    # Center the FileCleanerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    Cleaner_frame = MonitorFrame(app)
    Cleaner_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # You can access widgets/data like this:
    # print(Cleaner_frame.depth_var.get())

    app.mainloop()
