import customtkinter
import header
import greatings
import snapshots
import tools
import footer


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Toolkit")
        self.geometry("550x800")
        self.grid_columnconfigure(0, weight=1)

        self.header = header.HeaderFrame(self)
        self.header.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.greatings = greatings.GreatingsFrame(self)
        self.greatings.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        
        self.snapshots = snapshots.SnapshotsFrame(self)
        self.snapshots.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.snapshots.sheduleUpdates(self)

        self.tools = tools.ToolsFrame(self)
        self.tools.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.footer = footer.FooterFrame(self, version="1.0.0")
        self.footer.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def button_callback(self):
        print("button pressed")
