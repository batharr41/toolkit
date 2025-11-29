import customtkinter as ctk
from PIL import Image
import os

ICON_SIZE = (20, 20)
get_img = lambda x: ctk.CTkImage(Image.open(os.path.join("assets", x)), size=ICON_SIZE)
icon_map = {
    "photo": get_img("photo_icon.png"),
    "video": get_img("video_icon.png"),
    "document": get_img("documents_icon.png"),
    "audio": get_img("audio_icon.png"),
    "help": get_img("help_icon.png"),
    "add": get_img("add_icon.png"),
    "file": get_img("file_icon.png"),
    "delete": get_img("delete_icon.png"),
}


class VaultFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.files = [
            {"name": "photo.jpg", "type": "photo"},
            {"name": "video.mp4", "type": "video"},
            {"name": "document.pdf", "type": "document"},
            {"name": "audio.mp3", "type": "audio"},
            {
                "name": "another_file.zip",
                "type": "document",
            },  # Additional item for scroll test
            {
                "name": "vacation.png",
                "type": "photo",
            },  # Additional item for scroll test
        ]

        # --- 1. Title ---
        self.title_label = ctk.CTkLabel(
            self, text="Vault", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # --- 2. Action Buttons ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.add_button = ctk.CTkButton(
            self.button_frame,
            text=" Add File",
            image=icon_map["add"],
            compound="left",
            command=self.add_file_command,
        )
        self.add_button.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.help_button = ctk.CTkButton(
            self.button_frame,
            text=" Help",
            image=icon_map["help"],
            compound="left",
            command=self.help_command,
            fg_color=(
                "gray70",
                "gray30",
            ),
        )
        self.help_button.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

        # --- 3. Section Title ---
        self.files_title = ctk.CTkLabel(
            self,
            text="Stored Files",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )
        self.files_title.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")

        # --- 4. Scrollable Frame for File List ---
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.rows = []
        self._render_file_list()

    def delete_rows(self):
        for row in self.rows:
            for item in row:
                item.destroy()

    def _render_file_list(self):
        """Dynamically creates the list of files in the scrollable frame."""
        for i, file in enumerate(self.files):
            # Row frame
            frame = ctk.CTkFrame(self.scroll_frame)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(row=i, column=0, sticky="ew")

            file_icon = icon_map.get(file["type"], icon_map["file"])

            # The file label contains the icon and the file name
            file_label = ctk.CTkLabel(
                frame,
                text=f"  {file['name']}",
                image=file_icon,
                compound="left",
                anchor="w",
                font=ctk.CTkFont(size=16),
                padx=10,
                pady=5,
            )
            file_label.grid(row=0, column=0, sticky="ew")

            # Add a hover effect for better UX (optional)
            file_label.bind(
                "<Enter>",
                lambda event, label=file_label: label.configure(
                    fg_color=("gray80", "gray20")
                ),
            )
            file_label.bind(
                "<Leave>",
                lambda event, label=file_label: label.configure(fg_color="transparent"),
            )
            # delete button
            delete_but = ctk.CTkButton(
                frame,
                text="",
                image=icon_map["delete"],
                width=50,
                fg_color="transparent",
            )

            delete_but.grid(row=0, column=1, sticky="ew")
            delete_but.bind(
                "<Button-1>", lambda event, pos=i: print("Clicked but:" + str(pos))
            )

            self.rows.append((frame, file_label, delete_but))
        
    def add_file_command(self):
        print("Add File button clicked.")
        # Logic to open file dialog and add file...

    def help_command(self):
        print("Help button clicked.")
        # Logic to display help/documentation...


class VaultWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("File Organizer")
        self.geometry("550x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = VaultFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("Organizer App")
    app.geometry("550x600")

    # Center the FileOrganizerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    organizer_frame = VaultFrame(app)
    organizer_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    # You can access widgets/data like this:
    # print(organizer_frame.depth_var.get())

    app.mainloop()
