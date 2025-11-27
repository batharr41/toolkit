import customtkinter
from PIL import Image

class ToolsCell(customtkinter.CTkFrame):
    def __init__(self, master, filename, value, subValue):
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

        # value
        self.title = customtkinter.CTkLabel(
            self,
            text=value,
            font=("Helvetica", 20),
        )
        self.title.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="we")

        # title
        self.title = customtkinter.CTkLabel(
            self,
            text=subValue,
            font=("Helvetica", 16),
            text_color="gray50",
        )
        self.title.grid(row=2, column=0, padx=10, pady=(5, 5), sticky="we")


class ToolsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent",
        )
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
        self.orgnizerCell = ToolsCell(self.frame, "file.png", "File Organizer", "Organize folders")
        self.orgnizerCell.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.cleanerCell = ToolsCell(self.frame, "cleaner.png", "Cleaner", "Clear temp/cache")
        self.cleanerCell.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        self.monitorCell = ToolsCell(self.frame, "monitor.png", "System Monitor", "CPU,RAM,processes")
        self.monitorCell.grid(row=0, column=2, padx=5, pady=5, sticky="news")

        self.vaultCell = ToolsCell(self.frame, "vault.png", "Vault", "Store files safely")
        self.vaultCell.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.statsCell = ToolsCell(self.frame, "stats.png", "Stats Center", "Network,weather,etc")
        self.statsCell.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        self.settingsCell = ToolsCell(self.frame, "settings2.png", "Settings", "Preferences")
        self.settingsCell.grid(row=1, column=2, padx=5, pady=5, sticky="news")
