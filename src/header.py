import customtkinter
from PIL import Image


class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # LOGO
        imageData = Image.open("assets/icon.png")
        logo = customtkinter.CTkImage(
            dark_image=imageData, light_image=imageData, size=(50, 50)
        )
        self.logo = customtkinter.CTkLabel(
            self,
            text="",
            image=logo,
        )
        self.logo.pack(side="left", padx=10, pady=10)

        # Title
        self.title = customtkinter.CTkLabel(
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
        setting = customtkinter.CTkImage(
            dark_image=imageData2, light_image=imageData2, size=(40, 40)
        )
        self.settings = customtkinter.CTkLabel(
            self,
            text="",
            image=setting,
        )
        self.settings.pack(side="left", padx=10, pady=10)

        
