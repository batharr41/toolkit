import customtkinter
import app
import logic.utils as utils

# Themes: "blue" (standard), "green", "dark-blue"

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

if utils.is_linux():
    customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes"
    pass

app = app.App()
app.mainloop()
