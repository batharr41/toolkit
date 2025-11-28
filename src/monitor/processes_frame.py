import customtkinter as ctk
import psutil
import threading
from typing import List, Dict, Any, Tuple

# Set up appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")


class ProcessesFrame(ctk.CTkFrame):
    """
    A customtkinter application to display live CPU and RAM usage
    for top system processes using the psutil library.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # --- Configuration ---
        self.update_interval_ms = 1500
        self.max_processes = 15

        # State variables for threading and UI reuse
        self.is_fetching = False
        # Stores rows of (name_label, pid_label, cpu_label, mem_label)
        self.process_widgets: List[
            Tuple[ctk.CTkLabel, ctk.CTkLabel, ctk.CTkLabel, ctk.CTkLabel]
        ] = []

        # Configure grid for dynamic resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Real-Time Process Activity",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Container for the process list (Scrollable Frame)
        self.process_frame = ctk.CTkScrollableFrame(self, label_text="Top Processes")
        self.process_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        # Ensure the name column (0) gets most space
        self.process_frame.grid_columnconfigure(0, weight=3)
        self.process_frame.grid_columnconfigure((1, 2, 3), weight=1)

        # Setup Header Row
        self._setup_header()

        # --- Start Monitoring ---
        # Start the scheduling loop
        self._schedule_update()

    def _setup_header(self):
        """Creates the header row for the process table."""
        header_font = ctk.CTkFont(size=14, weight="bold")

        # Process Name
        ctk.CTkLabel(self.process_frame, text="Process Name", font=header_font).grid(
            row=0, column=0, padx=10, pady=(5, 10), sticky="w"
        )

        # Process ID (PID)
        ctk.CTkLabel(self.process_frame, text="PID", font=header_font).grid(
            row=0, column=1, padx=5, pady=(5, 10), sticky="w"
        )

        # CPU Usage
        ctk.CTkLabel(self.process_frame, text="CPU (%)", font=header_font).grid(
            row=0, column=2, padx=10, pady=(5, 10), sticky="e"
        )

        # RAM Usage
        ctk.CTkLabel(self.process_frame, text="RAM (%)", font=header_font).grid(
            row=0, column=3, padx=10, pady=(5, 10), sticky="e"
        )

    def _fetch_process_data(self) -> List[Dict[str, Any]]:
        """Retrieves and sorts process data using psutil."""
        processes = []

        # Initial call to cpu_percent to prime the pump (non-blocking)
        # This is a good practice to ensure the first results are meaningful deltas.
        psutil.cpu_percent(interval=None)

        # Iterate over all running processes
        for proc in psutil.process_iter(["name", "pid", "memory_percent"]):
            try:
                proc_info = proc.info
                # Calculate CPU percent over a small interval (0.0 means non-blocking,
                # retrieving the delta since the last time it was called.)
                cpu_percent = proc.cpu_percent(interval=0.0)

                # Filter out processes with very low activity
                if cpu_percent > 0.0 or proc_info["memory_percent"] > 0.0:
                    processes.append(
                        {
                            "name": proc_info["name"],
                            "pid": proc_info["pid"],
                            "cpu": cpu_percent,
                            "mem": proc_info["memory_percent"],
                        }
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Handle transient errors gracefully
                continue

        # Sort by CPU usage descending and return the top N processes
        processes.sort(key=lambda x: x["cpu"], reverse=True)
        return processes[: self.max_processes]

    def _thread_fetch_data(self):
        """Runs the blocking psutil call in a separate thread."""
        try:
            processes = self._fetch_process_data()

            # Once data is ready, schedule the UI update back on the main thread
            # Use 'after' to safely communicate results back to the main thread
            self.after(10, lambda: self._data_ready(processes))
        except Exception as e:
            print(f"Monitor Thread Error: {e}")
            self._data_ready([])  # Pass empty list on failure

    def _data_ready(self, processes: List[Dict[str, Any]]):
        """Called on the main thread when data fetching is complete."""
        self._update_ui(processes)
        self.is_fetching = False

    def _update_ui(self, processes: List[Dict[str, Any]]):
        """Updates or creates UI elements to display the new process data without flicker."""

        num_new_processes = len(processes)
        num_existing_widgets = len(self.process_widgets)

        # 1. Manage widget rows (Creation or Destruction)

        # A. Destroy excess rows if the number of processes decreased
        if num_existing_widgets > num_new_processes:
            for i in range(num_new_processes, num_existing_widgets):
                for widget in self.process_widgets[i]:
                    widget.destroy()
            # Truncate the list of managed widgets
            self.process_widgets = self.process_widgets[:num_new_processes]

        # B. Create new rows if the number of processes increased
        for i in range(num_existing_widgets, num_new_processes):
            row = i + 1
            # Create a tuple of the 4 labels needed for a process row
            widgets = (
                ctk.CTkLabel(self.process_frame, text="", anchor="w"),  # Name
                ctk.CTkLabel(self.process_frame, text="", anchor="w"),  # PID
                ctk.CTkLabel(self.process_frame, text="", anchor="e"),  # CPU
                ctk.CTkLabel(self.process_frame, text="", anchor="e"),  # RAM
            )
            # Layout the new widgets
            widgets[0].grid(row=row, column=0, padx=10, pady=2, sticky="w")
            widgets[1].grid(row=row, column=1, padx=5, pady=2, sticky="w")
            widgets[2].grid(row=row, column=2, padx=10, pady=2, sticky="e")
            widgets[3].grid(row=row, column=3, padx=10, pady=2, sticky="e")
            self.process_widgets.append(widgets)

        # 2. Update existing and newly created rows
        default_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        for i, proc in enumerate(processes):
            name_label, pid_label, cpu_label, mem_label = self.process_widgets[i]

            # Update the text using .configure() for flicker-free update
            name_label.configure(text=proc["name"])
            pid_label.configure(text=str(proc["pid"]))
            cpu_label.configure(text=f"{proc['cpu']:.1f}%")
            mem_label.configure(text=f"{proc['mem']:.1f}%")

            # Optional: Highlight high CPU usage
            if proc["cpu"] > 10.0:
                cpu_label.configure(text_color="#FF4500")  # OrangeRed
            elif proc["cpu"] > 5.0:
                cpu_label.configure(text_color="#FFD700")  # Gold
            else:
                cpu_label.configure(text_color=default_color)

    def _schedule_update(self):
        """Schedules the data fetch to run in a thread and reschedules itself."""
        # Only start a new fetch thread if the previous one is finished
        if not self.is_fetching:
            self.is_fetching = True
            # Start the thread, set daemon=True so it exits when the main app exits
            threading.Thread(target=self._thread_fetch_data, daemon=True).start()

        # Reschedule the scheduler itself to maintain the update interval
        self.after(self.update_interval_ms, self._schedule_update)
