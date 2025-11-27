import customtkinter as ctk
from .tools_header import ToolsHeader

class FoldersFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Folders to Organize Section ---
        self.folders_label = ctk.CTkLabel(
            self,
            text="Folders to Organize",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.folders_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        # Checkboxes (using instance variables for easy access/state checking)
        self.checkboxs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.checkboxs_frame.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")

        self.folders = ["Downloads", "Documents", "Desktop"]
        self.checks = []
        self.vars = []
        for fold in self.folders:
            var = ctk.StringVar(value="on")
            check = ctk.CTkCheckBox(
                self.checkboxs_frame,
                text=fold,
                variable=var,
                onvalue="on",
                offvalue="off",
            )
            check.pack(padx=20, pady=(10, 5))
            self.checks.append(check)
            self.vars.append(var)

        # Add Folder Button
        self.add_folder_button = ctk.CTkButton(self, text="Add Folder")
        self.add_folder_button.grid(
            row=3, column=0, padx=20, pady=(10, 20), sticky="we"
        )


class FileOrganizerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")

        # Configure the grid layout for the frame
        # Use column 0 for labels/widgets, and configure it to fill the space slightly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)  # Row for the Logs textbox should expand

        # --- 1. Title ---
        self.header = ToolsHeader(self,"file.png","File Organizer")
        self.header.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="n")

        # --- 1. Folder Contains
        self.folders = FoldersFrame(self)
        self.folders.grid(row=1, column=0, sticky="ewns")

        # --- 3. Search Depth Section ---
        self.depth_label = ctk.CTkLabel(
            self, text="Search Depth", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.depth_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        # ComboBox for Search Depth
        depth_options = ["1 level", "2 levels", "3 levels"]
        self.depth_var = ctk.StringVar(value="2 levels")  # Default value
        self.depth_combo = ctk.CTkComboBox(
            self, values=depth_options, variable=self.depth_var, state="readonly"
        )
        self.depth_combo.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")

        # --- 4. Start Button ---
        self.start_button = ctk.CTkButton(
            self, text="Start", fg_color="green", hover_color="darkgreen"
        )
        self.start_button.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

        # --- 5. Logs Section ---
        self.logs_label = ctk.CTkLabel(
            self, text="Logs", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.logs_label.grid(row=5, column=0, padx=20, pady=(10, 5), sticky="w")

        # Textbox for Logs
        # The row configured with weight=1 (row 9 in the layout above) is the logs section,
        # so this textbox will expand into the remaining vertical space.
        self.logs_textbox = ctk.CTkTextbox(self, height=100)
        self.logs_textbox.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="nsew")


class OrganizerWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("File Organizer")
        self.geometry("400x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = FileOrganizerFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("Organizer App")
    app.geometry("400x700")

    # Center the FileOrganizerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    organizer_frame = FileOrganizerFrame(app)
    organizer_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # You can access widgets/data like this:
    # print(organizer_frame.depth_var.get())

    app.mainloop()
