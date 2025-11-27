import psutil
import time
import platform  # Used for OS-specific adjustments
from typing import TypedDict


class SystemMetrics(TypedDict):
    cpu_used: str
    cpu_temp: str
    ram_used: str
    ram_gb: str
    disk_used: str
    disk_gb: str
    network_speed: str


def get_system_metrics():
    """
    Returns a dictionary containing key system hardware metrics.
    """

    # 1. CPU Usage
    # Get a 1-second average for more accurate usage reading
    cpu_percent = psutil.cpu_percent(interval=1)

    # 2. CPU Temperature (Less reliable across all OSes)
    cpu_temp = "N/A"
    try:
        # psutil's sensors_temperatures() is the standard way
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            # Common label for main CPU temperature on Linux/macOS
            cpu_temp = f"{temps['coretemp'][0].current:.1f} °C"
        elif "cpu_thermal" in temps:
            # Another common label (e.g., Raspberry Pi)
            cpu_temp = f"{temps['cpu_thermal'][0].current:.1f} °C"
        elif platform.system() == "Windows":
            # Windows temperature retrieval is often unsupported by psutil directly.
            pass

    except AttributeError:
        # Handles systems where sensors_temperatures() is not implemented (e.g., some Windows/VMs)
        cpu_temp = "Requires third-party tool on this OS"

    # 3. RAM Usage
    ram = psutil.virtual_memory()
    ram_used_percent = ram.percent
    # Convert bytes to Gigabytes (GB)
    ram_used_gb = ram.used / (1024**3)

    # 4. Disk Usage (for the root/primary partition)
    disk = psutil.disk_usage("/")
    disk_used_percent = disk.percent
    disk_used_gb = disk.used / (1024**3)

    # 5. Network Speed (Approximate download speed)
    # Get initial byte counts
    net_io_start = psutil.net_io_counters()
    time.sleep(1)  # Wait 1 second
    net_io_end = psutil.net_io_counters()

    # Calculate bytes received (download) over the interval
    download_bytes_per_sec = net_io_end.bytes_recv - net_io_start.bytes_recv
    # Convert bytes/sec to Megabits/sec (Mbps) for speed reporting
    # 1 Byte = 8 bits. 1 Megabit = 1,000,000 bits.
    network_speed_mbps = (download_bytes_per_sec * 8) / (1000**2)

    # Build the final dictionary
    metrics: SystemMetrics = {
        "cpu_used": f"{cpu_percent}%",
        "cpu_temp": f"Temp: {cpu_temp}",
        "ram_used": f"{ram_used_percent}%",
        "ram_gb": f"Used: {ram_used_gb:.0f}GB",
        "disk_used": f"{disk_used_percent}%",
        "disk_gb": f"Used: {disk_used_gb:.0f}GB",
        "network_speed": f"{network_speed_mbps:.0f}Mbps",
    }

    return metrics


# Run the function and print the result
if __name__ == "__main__":
    system_data = get_system_metrics()
    print(system_data)
