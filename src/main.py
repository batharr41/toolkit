import customtkinter
import app

# Themes: "blue" (standard), "green", "dark-blue"

customtkinter.set_default_color_theme("dark-blue")  
customtkinter.set_appearance_mode("dark")

customtkinter.DrawEngine.preferred_drawing_method = "circle_shapes"

app = app.App()
app.mainloop()