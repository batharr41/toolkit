# **🛠️ Toolkit: System Utilities Suite**

## **🌟 Project Overview**

**Toolkit** is a comprehensive, cross-platform desktop application designed to streamline system maintenance, file management, and real-time performance monitoring. 

The application is structured around a central dashboard (Toolkit) that provides immediate system snapshots and acts as a hub for accessing six core utility modules.

## **✨ Features and Tools**

Toolkit is divided into several specialized modules, accessible from the main dashboard:

### **1\. Toolkit (Dashboard)**

The main landing page provides an immediate status report on critical system components:

* **System Snapshots:** A quick, static view of current CPU, RAM, Disk usage, and Network activity.  
* **Real-Time Process Activity:** Lists the Top Processes currently running, showing real-time metrics for Process Name, PID, CPU (%), and RAM (%). **This data auto-refreshes rapidly to ensure accuracy.**

### **2\. System Monitor**

The dedicated monitoring page provides a deep dive into active processes and resource consumption, offering a comprehensive, rapidly updating view of system health.

### **3\. Stats Center**

This module focuses on network and geographic data, providing utility information about the user's connection and local environment.

* **Network Status:** Displays the public IP Address, Location (City, Country), and Internet Service Provider (ISP).  
* **Weather Data:** Shows the current local temperature and a 5-day forecast.  
* **Auto-Refresh:** Like the System Monitor, **all data on this page refreshes rapidly** to ensure the most current network and weather information is displayed.

### **4\. File Cleaner**

A dedicated tool for system hygiene and freeing up disk space.

* **Cleaning Options:** Allows the user to select specific targets for cleaning:  
  * Temporary Files  
  * Browser Cache  
  * Large & Old Files

### **5\. File Organizer**

Helps maintain a tidy file system by automatically sorting files into designated directories.

* **Folders to Organize:** Users can specify which folders to target, with common defaults like Downloads, Documents, and Desktop provided.  
* **Search Depth:** Configurable depth to control how deep the organizer looks into subdirectories.

### **6\. Vault**

A secure section designed for storing and managing sensitive documents and files.

* **Secure Storage:** Allows users to add and manage files within a protected area.

## **🛠️ Skills and Tools Used**

This project showcases proficiency in Python development, GUI design, and system-level interaction.

| Category | Technology / Library | Description |
| :---- | :---- | :---- |
| **Core Language** | Python 3.10.2+ | The primary programming language for all back-end logic and application structure. |
| **GUI Framework** | custom-tkinter | Used for creating the modern, highly customizable, and cross-platform graphical user interface, giving the app its unique aesthetic. |
| **System Monitoring** | psutil  | Library used to gather real-time data on CPU, RAM, Disk, Network, and Process activity. |
| **File Management** | os, shutil | Standard Python libraries for interacting with the file system (cleaning, organizing, moving files). |
| **Networking/Data** | requests, APIs (OpenWeatherMap, IP Geolocation) | Used for fetching external data such as location, ISP information, and current weather forecasts. |
| **Platform** | Linux (Primary Dev Environment) | Developed to be functional on Linux, with cross-platform considerations for Python and custom-tkinter. |
| **Design** | Custom UI/UX | Implementation of a cohesive, visually appealing, and highly legible dark-themed interface. |

## **⚙️ Installation Guide**

To run Toolkit locally, you must have Python 3.10 or newer installed on your system.

### **Prerequisites**

* Python 3.10+  
* pip (Python package installer)

### **Step 1: Clone the Repository**

git clone \<YOUR\_REPOSITORY\_URL\_HERE\>  
cd toolkit-suite

### **Step 2: Install Dependencies**

While the specific names might vary, the primary libraries include custom-tkinter and likely psutil for system monitoring.

\# It is highly recommended to use a virtual environment  
python3 \-m venv venv  
source venv/bin/activate  \# On Linux/macOS  
\# .\\venv\\Scripts\\activate \# On Windows

\# Install required libraries  
pip install custom-tkinter psutil requests \# Add any other specific libraries you use

### **Step 3: Run the Application**

Execute the main Python file to start the Toolkit.

python3 main\_toolkit.py \# Replace main\_toolkit.py with your actual entry file name

## **🖥️ Usage**

1. **Launch:** Start the application using the command above.  
2. **Dashboard:** The main screen provides a system overview and navigation buttons.  
3. **Real-Time Data:** Navigate to **System Monitor** and **Stats Center** to view data that updates every few seconds.  
4. **Utilities:** Click on **File Cleaner** or **File Organizer**, configure your settings (e.g., selection checkboxes, folder paths), and click **Start** (or the equivalent action button) to execute the task.


*Author: Bather Bilal* *Release Date: December 2025*