import customtkinter as ctk
from PIL import Image


class ToolsHeader(ctk.CTkFrame):
    def __init__(self, master, filename: str, title: str):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)

        # image
        imageData = Image.open(f"assets/{filename}")
        logo = ctk.CTkImage(dark_image=imageData, light_image=imageData, size=(50, 50))
        self.logo = ctk.CTkLabel(
            self,
            text="",
            image=logo,
        )
        self.logo.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.title_label = ctk.CTkLabel(
            self, text=title, font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=(10, 10), sticky="wns")
