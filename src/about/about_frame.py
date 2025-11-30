import customtkinter as ctk
import platform
from orginizer.tools_header import ToolsHeader

# --- Configuration ---
ctk.set_appearance_mode("Dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
ctk.DrawEngine.preferred_drawing_method = "circle_shapes"


class AboutFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Set a common padding value
        PAD_X = 20
        PAD_Y = 10

        # --- App Info Data Structure ---
        self.app_info_data = {
            "Name": "Toolkit",
            "Version": "1.0.0",
            "Author": "Bathar Bilal",
            "Release": "Dec 2025",
        }

        # --- Platform Data Structure ---
        self.platform_data = {
            "Python": "3.13.2",
            "GUI Library": "customtkinter",
            "OS": platform.system(),
            "UI Framework": "customtkinter",
        }

        # Configure grid for the main window (1 column)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((2, 4), weight=1)

        # 1. Header Section
        self.header = ToolsHeader(self, "settings2.png", "About")
        self.header.grid(row=0, column=0, padx=PAD_X, pady=(20, 10), sticky="ew")

        # 2. App Info Section

        self.app_info_label = ctk.CTkLabel(
            self, text="App Info", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.app_info_label.grid(
            row=1, column=0, padx=PAD_X, pady=(PAD_Y, 5), sticky="w"
        )

        # Frame for App Info content
        self.app_info_frame = ctk.CTkFrame(self)
        self.app_info_frame.grid(
            row=2, column=0, padx=PAD_X, pady=(0, PAD_Y * 2), sticky="ew"
        )
        self.app_info_frame.grid_columnconfigure(0, weight=1)  # Key
        self.app_info_frame.grid_columnconfigure(1, weight=1)  # Value

        self.create_info_rows(self.app_info_frame, self.app_info_data, start_row=0)

        # ---

        # 3. Platform Data Section

        self.platform_data_label = ctk.CTkLabel(
            self, text="Platform Data", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.platform_data_label.grid(
            row=3, column=0, padx=PAD_X, pady=(PAD_Y, 5), sticky="w"
        )

        # Frame for Platform Data content
        self.platform_data_frame = ctk.CTkFrame(self)
        self.platform_data_frame.grid(
            row=4, column=0, padx=PAD_X, pady=(0, 20), sticky="ew"
        )
        self.platform_data_frame.grid_columnconfigure(0, weight=1)  # Key
        self.platform_data_frame.grid_columnconfigure(1, weight=1)  # Value

        self.create_info_rows(self.platform_data_frame, self.platform_data, start_row=0)

    def create_info_rows(self, parent_frame, data_dict, start_row):
        """Helper function to create the key-value rows."""

        row_index = start_row

        for key, value in data_dict.items():
            # Label for the Key (left side, slightly dimmed)
            key_label = ctk.CTkLabel(
                parent_frame,
                text=key,
                font=ctk.CTkFont(size=14),
                anchor="w",
                text_color="#A9A9A9",  # Lighter grey for the key
            )
            key_label.grid(row=row_index, column=0, padx=15, pady=5, sticky="w")

            # Label for the Value (right side, main color, bold for emphasis)
            value_label = ctk.CTkLabel(
                parent_frame,
                text=value,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="e",
            )
            # Use 'e' (east) sticky to push the text to the right side of the column
            value_label.grid(row=row_index, column=1, padx=15, pady=5, sticky="e")

            row_index += 1


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("About")
        self.geometry("400x520")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = AboutFrame(self)
        self.frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("Cleaner App")
    app.geometry("400x520")

    # Center the FileCleanerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    Cleaner_frame = AboutFrame(app)
    Cleaner_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    # You can access widgets/data like this:
    # print(Cleaner_frame.depth_var.get())

    app.mainloop()
