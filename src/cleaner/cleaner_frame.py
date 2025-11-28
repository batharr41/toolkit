import customtkinter as ctk
from orginizer.tools_header import ToolsHeader
from .folders_framer import FoldersFrame
from .cleaner_helper import run_clean_logic


class FileCleanerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="transparent")

        # Configure the grid layout for the frame
        # Use column 0 for labels/widgets, and configure it to fill the space slightly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Row for the Logs textbox should expand

        # --- 1. Title ---
        self.header = ToolsHeader(self, "cleaner.png", "File Cleaner")
        self.header.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="n")

        # --- 2. Folder Contains
        self.folders = FoldersFrame(self)
        self.folders.grid(row=1, column=0, sticky="ewns")

        # --- 3. Start Button ---
        self.start_button = ctk.CTkButton(
            self,
            text="Start",
            fg_color="green",
            hover_color="darkgreen",
            command=self.on_clean,
        )
        self.start_button.grid(row=2, column=0, padx=20, pady=(40, 20), sticky="ew")

        # --- 5. Logs Section ---
        self.logs_label = ctk.CTkLabel(
            self, text="Logs", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.logs_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")

        # Textbox for Logs
        # The row configured with weight=1 (row 9 in the layout above) is the logs section,
        # so this textbox will expand into the remaining vertical space.
        self.logs_textbox = ctk.CTkTextbox(self, height=100)
        self.logs_textbox.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="nsew")

    def addLog(self, log):
        info = self.logs_textbox.get("1.0", "end")
        info += f"\n{log}"
        self.logs_textbox.delete("1.0", "end")
        self.logs_textbox.insert("1.0", info)
        print(log)

    def on_clean(self):
        self.logs_textbox.delete("1.0", "end")
        folders = self.folders.get_folders()
        options = {
            "temp_files": self.folders.folders[0] in folders,
            "browser_cache": self.folders.folders[1] in folders,
            "large_old": self.folders.folders[0] in folders,
        }
        run_clean_logic(options, lambda x: self.addLog(x))


class CleanerWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("File Cleaner")
        self.geometry("500x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = FileCleanerFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("Cleaner App")
    app.geometry("400x700")

    # Center the FileCleanerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    Cleaner_frame = FileCleanerFrame(app)
    Cleaner_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # You can access widgets/data like this:
    # print(Cleaner_frame.depth_var.get())

    app.mainloop()
