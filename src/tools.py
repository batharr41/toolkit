import customtkinter
from PIL import Image
from orginizer.organize_frame import OrganizerWindow
from cleaner.cleaner_frame import CleanerWindow
from monitor.monitor_frame import MonitorWindow


class ToolsCell(customtkinter.CTkFrame):
    def __init__(self, master, filename, value, subValue, command):
        super().__init__(
            master,
            corner_radius=10,
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # image
        imageData = Image.open(f"assets/{filename}")
        logo = customtkinter.CTkImage(
            dark_image=imageData, light_image=imageData, size=(50, 50)
        )
        self.logo = customtkinter.CTkLabel(
            self,
            text="",
            image=logo,
        )
        self.logo.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.logo.bind("<Button-1>", command)

        # value
        self.value = customtkinter.CTkLabel(
            self,
            text=value,
            font=("Helvetica", 20),
        )
        self.value.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="we")
        self.value.bind("<Button-1>", command)

        # title
        self.subvalue = customtkinter.CTkLabel(
            self,
            text=subValue,
            font=("Helvetica", 16),
            text_color="gray50",
        )
        self.subvalue.grid(row=2, column=0, padx=10, pady=(5, 5), sticky="we")
        self.subvalue.bind("<Button-1>", command)

        self.bind("<Button-1>", command)


class ToolsFrame(customtkinter.CTkFrame):

    window: customtkinter.CTk
    fileorganizer: customtkinter.CTkToplevel
    cleaner: customtkinter.CTkToplevel
    monitor: customtkinter.CTkToplevel

    def __init__(self, window):
        super().__init__(
            window,
            fg_color="transparent",
        )
        self.window = window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Title
        self.title = customtkinter.CTkLabel(self, text=f"Tools", font=("Helvetica", 24))
        self.title.grid(row=0, column=0, padx=10, pady=(15, 10), sticky="w")

        # row
        self.frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame.grid(
            row=1,
            column=0,
            sticky="we",
        )
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1), weight=1)

        # cells
        self.orgnizerCell = ToolsCell(
            self.frame,
            "file.png",
            "File Organizer",
            "Organize folders",
            self.open_fileorganizer,
        )
        self.orgnizerCell.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.cleanerCell = ToolsCell(
            self.frame,
            "cleaner.png",
            "Cleaner",
            "Clear temp/cache",
            self.open_cleaner,
        )
        self.cleanerCell.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        self.monitorCell = ToolsCell(
            self.frame,
            "monitor.png",
            "System Monitor",
            "CPU,RAM,processes",
            self.open_monitor,
        )
        self.monitorCell.grid(row=0, column=2, padx=5, pady=5, sticky="news")

        self.vaultCell = ToolsCell(
            self.frame,
            "vault.png",
            "Vault",
            "Store files safely",
            self.open_fileorganizer,
        )
        self.vaultCell.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.statsCell = ToolsCell(
            self.frame,
            "stats.png",
            "Stats Center",
            "Network,weather,etc",
            self.open_fileorganizer,
        )
        self.statsCell.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        self.settingsCell = ToolsCell(
            self.frame,
            "settings2.png",
            "Settings",
            "Preferences",
            self.open_fileorganizer,
        )
        self.settingsCell.grid(row=1, column=2, padx=5, pady=5, sticky="news")

        # popups
        self.fileorganizer = None
        self.cleaner = None
        self.monitor = None

    def open_fileorganizer(self, ev):
        if self.fileorganizer is None or not self.fileorganizer.winfo_exists():
            self.fileorganizer = OrganizerWindow(self.window)
        else:
            self.fileorganizer.focus()

    def open_cleaner(self, ev):
        if self.cleaner is None or not self.cleaner.winfo_exists():
            self.cleaner = CleanerWindow(self.window)
        else:
            self.cleaner.focus()

    def open_monitor(self, ev):
        if self.monitor is None or not self.monitor.winfo_exists():
            self.monitor = MonitorWindow(self.window)
        else:
            self.monitor.focus()
