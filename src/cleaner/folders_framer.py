import customtkinter as ctk
from typing import TypedDict


class FoldersFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Folders to Organize Section ---
        self.folders_label = ctk.CTkLabel(
            self,
            text="Cleaning Options",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.folders_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        # Checkboxes (using instance variables for easy access/state checking)
        self.checkboxs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.checkboxs_frame.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")

        self.folders = ["Temp Files", "Browser Cache", "Large & Old files"]
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
            check.pack(padx=20, pady=(10, 5), expand=True, fill="x")
            self.checks.append(check)
            self.vars.append(var)

    def get_folders(self):
        res = []
        for i, fold in enumerate(self.folders):
            if self.vars[i].get() == "on":
                res.append(fold)

        return res
