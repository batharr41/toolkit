import customtkinter
import logic.utils as utils


class GreatingsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            corner_radius=10,
        )

        # Title
        username = utils.getUserName()
        self.title = customtkinter.CTkLabel(
            self,
            text=f"Hello, {username}👋",
            font=("Helvetica", 24),
        )
        self.title.pack(
            anchor="w",
            padx=30,
            pady=(10, 0),
            expand=True,
        )

        # Sub Title
        self.subtitle = customtkinter.CTkLabel(
            self,
            text=f"Your system is running normally.",
            font=("Helvetica", 18),
            text_color="gray50",
        )
        self.subtitle.pack(
            anchor="w",
            padx=30,
            pady=(5, 10),
            expand=True,
        )
