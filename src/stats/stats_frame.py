import customtkinter as ctk
from PIL import Image
from . import stats_helper
import threading
from orginizer.tools_header import ToolsHeader
import requests
from io import BytesIO

ctk.DrawEngine.preferred_drawing_method = "circle_shapes"


class NetworkFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.network_title = ctk.CTkLabel(
            self, text="Network", font=ctk.CTkFont(size=18, weight="bold")
        )

        # Network details
        network_data = {
            "IP Address": "192.168.1.10",
            "Location": "New York, USA",
            "ISP": "Verizon",
            "Public IP": "203.0.113.42",
        }
        self.labels: list[ctk.CTkLabel] = []
        for i, (key, value) in enumerate(network_data.items()):
            label_key = ctk.CTkLabel(self, text=key, font=ctk.CTkFont(size=14))
            label_key.grid(row=i + 1, column=0, padx=15, pady=5, sticky="w")
            label_value = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=14))
            label_value.grid(row=i + 1, column=1, padx=15, pady=5, sticky="e")
            self.labels.append(label_value)

    def set_data(self, data):
        ip_address = data.get("ip_address", "--")
        location = data.get("location", "--")
        isp = data.get("isp", "--")
        public_ip = data.get("public_ip", "--")
        values = [ip_address, location, isp, public_ip]
        for i, label in enumerate(self.labels):
            label.configure(text=values[i])


class ForecastFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)  # For forecast

        self.weather_title = ctk.CTkLabel(
            self, text="Weather", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.weather_title.grid(
            row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w"
        )

        # Current temperature
        self.temp_label = ctk.CTkLabel(
            self, text="23°C", font=ctk.CTkFont(size=48, weight="bold")
        )
        self.temp_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        # Weather icon and description
        self.current_weather_icon = ctk.CTkLabel(
            self, text="☀️", font=ctk.CTkFont(size=48)
        )
        self.current_weather_icon.grid(row=1, column=1, padx=15, pady=5, sticky="e")
        print(
            "Warning: 'cloud_sun.png' not found. Using text fallback for weather icon."
        )

        self.weather_desc_label = ctk.CTkLabel(
            self, text="Clouds", font=ctk.CTkFont(size=16)
        )
        self.weather_desc_label.grid(
            row=2, column=1, padx=15, pady=(0, 10), sticky="ne"
        )

        # 5-day forecast
        self.forecast_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.forecast_frame.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="ew"
        )
        for i in range(5):
            self.forecast_frame.grid_columnconfigure(i, weight=1)

        forecast_data = [
            {"day": "Mon", "icon": "☀️", "high": "25°", "low": "19°"},
            {"day": "Tue", "icon": "☀️", "high": "27°", "low": "20°"},
            {"day": "Wed", "icon": "☁️", "high": "28°", "low": "22°"},
            {"day": "Thu", "icon": "☁️", "high": "26°", "low": "21°"},
            {"day": "Fri", "icon": "🌧️", "high": "24°", "low": "21°"},
        ]

        self.cells: list[
            tuple[
                ctk.CTkLabel,
                ctk.CTkLabel,
                ctk.CTkLabel,
            ]
        ] = []
        for i, day_data in enumerate(forecast_data):
            day_frame = ctk.CTkFrame(self.forecast_frame, corner_radius=5)
            day_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            day_frame.grid_rowconfigure((0, 1, 2), weight=0)  # Day, Icon, Temps
            day_frame.grid_columnconfigure(0, weight=1)

            day_lbl = ctk.CTkLabel(
                day_frame,
                text=day_data["day"],
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            day_lbl.grid(row=0, column=0, pady=(5, 0))

            icon_lbl = ctk.CTkLabel(
                day_frame, text=day_data["icon"], font=ctk.CTkFont(size=24)
            )
            icon_lbl.grid(row=1, column=0)

            temp_lbl = ctk.CTkLabel(
                day_frame,
                text=f"{day_data['high']}\n{day_data['low']}",
                font=ctk.CTkFont(size=12),
            )
            temp_lbl.grid(row=2, column=0, pady=(0, 5))
            self.cells.append([day_lbl, icon_lbl, temp_lbl])

    def set_forecasts_list(self, forecasts):
        for i, forecast in enumerate(forecasts):
            cell = self.cells[i]
            cell[0].configure(text=forecast.get("day", "--"))
            try:
                response = requests.get(forecast.get("icon_url", ""), timeout=10)
                response.raise_for_status()
                image_data = BytesIO(response.content)
                image_pil = Image.open(image_data)
                image = ctk.CTkImage(
                    dark_image=image_pil, light_image=image_pil, size=(50, 50)
                )
                cell[1].configure(text="", image=image)
            except Exception as e:
                print("Get image failed", e)
            cell[2].configure(
                text=f"{forecast.get("low","--")}\n{forecast.get("high","--")}"
            )

    def set_data(self, data):
        try:
            response = requests.get(data.get("icon_url", ""), timeout=10)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            image_pil = Image.open(image_data)
            image = ctk.CTkImage(
                dark_image=image_pil, light_image=image_pil, size=(80, 80)
            )
            self.current_weather_icon.configure(text="", image=image)
        except Exception as e:
            print("get data image failed", e)
        self.temp_label.configure(text=data.get("high", "--"))
        self.weather_desc_label.configure(text=data.get("weather_main", "--"))


class StatsCenterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # Configure grid for main window
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Network frame
        self.grid_rowconfigure(2, weight=2)  # Weather frame
        self.grid_columnconfigure(0, weight=1)

        # --- 1. Title ---
        self.header = ToolsHeader(self, "stats.png", "Stats Center")
        self.header.grid(row=0, column=0, padx=20, pady=(0, 10), sticky="n")

        # --- Network Frame ---
        self.network_frame = NetworkFrame(self)
        self.network_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # --- Weather Frame ---
        self.weather_frame = ForecastFrame(self)
        self.weather_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.get_data()

    def get_data(self):

        def threaded_fetch():
            network, forecasts = stats_helper.get_network_and_forecast()
            today = forecasts[0]
            print("got", network, "forecast", forecasts, "todat", today)

            def update_ui():
                print("update-ui")
                self.network_frame.set_data(network)
                self.weather_frame.set_data(today)
                self.weather_frame.set_forecasts_list(forecasts)
                for f in forecasts:
                    print("ff:  ", f)

            self.after(0, update_ui)

        thread = threading.Thread(target=threaded_fetch, daemon=True)
        thread.start()


class StatsCenterWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Stats Center")
        self.geometry("500x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = StatsCenterFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")


# --- Example Usage (Main Application Loop) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Themes can be "System", "Dark", or "Light"
    ctk.set_default_color_theme("dark-blue")
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"

    app = ctk.CTk()
    app.title("Stats Center")
    app.geometry("500x600")

    # Center the FileCleanerFrame in the main window
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    stats_frame = StatsCenterFrame(app)
    stats_frame.grid(row=0, column=0, sticky="nsew")

    # You can access widgets/data like this:
    # print(stats_frame.depth_var.get())

    app.mainloop()
