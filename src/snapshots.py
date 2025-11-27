import customtkinter
import logic.stats as stats


class SnapshotsCell(customtkinter.CTkFrame):
    def __init__(self, master, title, value, subValue):
        super().__init__(
            master,
            corner_radius=10,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # title
        self.title = customtkinter.CTkLabel(
            self,
            text=title,
            font=("Helvetica", 22),
        )
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # value
        self.value = customtkinter.CTkLabel(
            self,
            text=value,
            font=("Helvetica", 28),
        )
        self.value.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        # title
        self.subvalue = customtkinter.CTkLabel(
            self,
            text=subValue,
            font=("Helvetica", 16),
            text_color="gray50",
        )
        self.subvalue.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

    def update(self, value: str, subvalue: str):
        self.value.configure(text=value)
        self.subvalue.configure(text=subvalue)


class SnapshotsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent",
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title = customtkinter.CTkLabel(
            self, text=f"System Snapshots", font=("Helvetica", 24)
        )
        self.title.grid(row=0, column=0, padx=10, pady=(15, 10), sticky="w")

        # row
        self.frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame.grid(
            row=1,
            column=0,
            sticky="we",
        )
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # cells
        self.cpuCell = SnapshotsCell(self.frame, "CPU", "22%", "Temp: 45deg")
        self.cpuCell.grid(row=0, column=0, padx=5, sticky="news")

        self.ramCell = SnapshotsCell(self.frame, "RAM", "22%", "Used: 7.4GB")
        self.ramCell.grid(row=0, column=1, padx=5, sticky="news")

        self.diskCell = SnapshotsCell(self.frame, "Disk", "22%", "Free 300GB")
        self.diskCell.grid(row=0, column=2, padx=5, sticky="news")

        self.networkCell = SnapshotsCell(self.frame, "Network", "12 Mbps", "Free")
        self.networkCell.grid(row=0, column=3, padx=5, sticky="news")
        
        self.updateStats()

    def updateStats(self):
        data = stats.get_system_metrics()
        self.cpuCell.update(data.get("cpu_used"), data.get("cpu_temp"))
        self.ramCell.update(data.get("ram_used"), data.get("ram_gb"))
        self.diskCell.update(data.get("disk_used"), data.get("disk_gb"))
        self.networkCell.update(data.get("network_speed"), data.get("Free"))

    def sheduleUpdates(self, window: customtkinter.CTk):

        def runUpdate():
            self.updateStats()
            self.sheduleUpdates(window)

        window.after(2500, runUpdate)
