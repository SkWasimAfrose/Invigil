import sys
import os
import threading
import customtkinter as ctk
import ctypes

from config import *
from PIL import Image

from monitor import (
    start_monitoring,
    stop_monitoring
)

from telegram_bot import (
    start_telegram_bot,
    set_current_student,
    stop_telegram_bot
)

# APP SETTINGS

ctk.set_appearance_mode(
    "dark"
)

ctk.set_default_color_theme(
    "blue"
)

# RESOURCE PATH

def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS

    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )

# MAIN WINDOW

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "invigil.app"
)

app = ctk.CTk()

app.iconbitmap(
    resource_path(
        "assets/invigil.ico"
    )
)

app.title(
    APP_TITLE
)

screen_width = app.winfo_screenwidth()

screen_height = app.winfo_screenheight()

x_position = int(
    (screen_width / 1.5)
    - (WINDOW_WIDTH / 1.5)
)

y_position = int(
    (screen_height / 5.5)
    - (WINDOW_HEIGHT / 5.5)
)

app.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    f"+{x_position}+{y_position}"
)

app.resizable(
    False,
    False
)

logo_image = ctk.CTkImage(
    light_image=Image.open(
        resource_path(
            "assets/invigil_logo.png"
        )
    ),
    dark_image=Image.open(
        resource_path(
            "assets/invigil_logo.png"
        )
    ),
    size=(90, 90)
)

telegram_updater = (
    start_telegram_bot()
)
monitoring_started = False
monitor_thread = None

# INPUT FILTERS

def filter_name(event):

    current_text = name_entry.get()

    filtered_text = "".join(

        char

        for char in current_text

        if (
            char.isalpha()
            or char.isspace()
        )
    )

    if current_text != filtered_text:

        name_entry.delete(
            0,
            "end"
        )

        name_entry.insert(
            0,
            filtered_text
        )

def filter_roll(event):

    current_text = roll_entry.get()

    filtered_text = "".join(

        char

        for char in current_text

        if char.isdigit()
    )

    if current_text != filtered_text:

        roll_entry.delete(
            0,
            "end"
        )

        roll_entry.insert(
            0,
            filtered_text
        )

# WINDOW CLOSE

def close_app():

    stop_monitoring()
    stop_telegram_bot()

    app.destroy()

app.protocol(
    "WM_DELETE_WINDOW",
    close_app
)

# START MONITORING

def launch_monitoring():

    global monitoring_started
    global monitor_thread
    
    student_name = (
        name_entry.get().strip()
    )

    roll_number = (
        roll_entry.get().strip()
    )

    if monitoring_started:

        return
    
    # VALIDATION

    if (
        not student_name
        or not roll_number
    ):

        status_label.configure(
            text="Please fill all fields",
            text_color="red"
        )

        return

    STUDENT_ID = (
        f"{roll_number}_{student_name}"
    )

    set_current_student(
    STUDENT_ID
    )
    
    # STATUS

    status_label.configure(
        text="Monitoring Started",
        text_color="green"
    )

    monitoring_started = True

    start_button.configure(
        state="disabled"
    )

    # THREAD START

    monitor_thread = threading.Thread(
        target=start_monitoring,
        args=(STUDENT_ID,),
        daemon=True
    )

    monitor_thread.start()

# LOGO

logo_label = ctk.CTkLabel(
    app,
    image=logo_image,
    text=""
)

logo_label.pack(
    pady=(25, 10)
)

# TITLE

title_label = ctk.CTkLabel(
    app,
    text="Exam Monitoring",
    font=("Arial", 28, "bold")
)

title_label.pack(
    pady=(0, 10)
)

# SUBTITLE

subtitle_label = ctk.CTkLabel(
    app,
    text="Student Monitoring Launcher",
    font=("Arial", 16)
)

subtitle_label.pack(
    pady=(0, 20)
)

# STUDENT NAME

name_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter Student Name"
)

name_entry.pack(
    pady=10
)

name_entry.bind(
    "<KeyRelease>",
    filter_name
)

name_entry.bind(
    "<Return>",
    lambda event: roll_entry.focus()
)

# ROLL NUMBER

roll_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter Roll Number"
)

roll_entry.pack(
    pady=10
)

roll_entry.bind(
    "<KeyRelease>",
    filter_roll
)

roll_entry.bind(
    "<Return>",
    lambda event: launch_monitoring()
)

# START BUTTON

start_button = ctk.CTkButton(
    app,
    text="Start Monitoring",
    width=250,
    height=45,
    command=launch_monitoring
)

start_button.pack(
    pady=(30, 15)
)

# STATUS LABEL

status_label = ctk.CTkLabel(
    app,
    text="Ready",
    font=("Arial", 14)
)

status_label.pack(
    pady=(0, 10)
)

# RUN APP

app.mainloop()