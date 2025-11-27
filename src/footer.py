import customtkinter


class FooterFrame(customtkinter.CTkFrame):
    """
    A custom frame designed to be placed at the bottom of the main application
    window, displaying version information on the left and a credit message on the right.
    """

    def __init__(self, master, version="1.0.0", **kwargs):
        super().__init__(
            master, corner_radius=10, fg_color=("gray85", "gray17"), **kwargs
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        font = ("Helvetica", 14)

        self.version_label = customtkinter.CTkLabel(
            self,
            text=f"Version {version}",
            font=font,
            text_color=("gray20", "gray80"),
        )
        self.version_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.credit_label = customtkinter.CTkLabel(
            self,
            text="Made with ❤️ in Python",
            font=font,
            text_color=("gray20", "gray80"),
        )
        self.credit_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")
