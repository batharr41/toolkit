import customtkinter as ctk
from PIL import Image
from about.about_frame import AboutWindow


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.about: ctk.CTkToplevel = None
        self.window: ctk.CTk = None

        # LOGO
        imageData = Image.open("assets/icon.png")
        logo = ctk.CTkImage(dark_image=imageData, light_image=imageData, size=(50, 50))
        self.logo = ctk.CTkLabel(
            self,
            text="",
            image=logo,
        )
        self.logo.pack(side="left", padx=10, pady=10)

        # Title
        self.title = ctk.CTkLabel(
            self,
            text="Toolkit",
            font=("Helvetica", 32, "bold"),
        )
        self.title.pack(
            anchor="w",
            side="left",
            padx=10,
            pady=10,
            expand=True,
        )

        # Settings
        imageData2 = Image.open("assets/setting.png")
        setting = ctk.CTkImage(
            dark_image=imageData2, light_image=imageData2, size=(40, 40)
        )
        self.settings = ctk.CTkLabel(
            self,
            text="",
            image=setting,
        )
        self.settings.pack(side="left", padx=10, pady=10)
        self.settings.bind("<Button-1>", self.open_about)

    def open_about(self, ev):
        if self.about is None or not self.about.winfo_exists():
            self.about = AboutWindow(self.window)
        else:
            self.about.focus()
