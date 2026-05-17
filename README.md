# Invigil

Invigil is a desktop-based exam monitoring system built using Python, OpenCV, MediaPipe, and Telegram Bot API.

The application monitors students during online exams using a webcam and automatically detects suspicious activities such as:

- Looking away repeatedly
- Leaving the camera
- Multiple people appearing on screen

When suspicious activity is detected, Invigil:

- sends Telegram alerts
- captures evidence images
- stores evidence locally

The project includes:

- modern GUI
- packaged EXE support
- Telegram integration
- evidence management system
- standalone deployment support

---

# Features

## Live Webcam Monitoring

Monitors student activity in real time using webcam input.

## Suspicious Side Movement Detection

Detects repeated left/right head movement patterns.

## Multiple Face Detection

Detects when more than one person appears in camera.

## Left Camera Detection

Detects when student leaves webcam view for a specific duration.

## Telegram Alerts

Sends real-time notifications directly to Telegram.

## Evidence Capture

Automatically saves evidence screenshots for suspicious activities.

## Modern GUI

Includes a branded modern desktop interface using CustomTkinter.

## Standalone EXE Support

Can run as standalone Windows executable without installing Python.

---

# Technologies Used

- Python
- OpenCV
- MediaPipe
- CustomTkinter
- Telegram Bot API
- Pillow
- PyInstaller

---

# Project Structure

```text
Invigil/
│
├── assets/
│   ├── invigil.ico
│   └── invigil_logo.png
│
├── evidence/
│
├── main.py
├── monitor.py
├── telegram_bot.py
├── evidence.py
├── config.py
├── requirements.txt
├── .env
└── README.md
```

---

# Requirements

Before running the project, install:

- Python 3.11 recommended
- Webcam
- Internet connection

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Invigil.git
```

---

## 2. Open Project Folder

```bash
cd Invigil
```

---

## 3. Create Virtual Environment

### Windows CMD

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows CMD

```bash
venv\Scripts\activate
```

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Telegram Bot Setup

Invigil uses Telegram Bot API for sending alerts.

---

## Step 1: Create Telegram Bot

1. Open Telegram
2. Search for:

```text
@BotFather
```

3. Create a new bot using:

```text
/newbot
```

4. Copy the generated bot token

---

## Step 2: Get Chat ID

1. Send a message to your bot
2. Open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

3. Find your:

```text
chat.id
```

value

---

# Environment Variables Setup

Create a file named:

```text
.env
```

inside project root.

Add:

```env
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```

Important:

- do not use quotes
- do not add spaces around `=`

---

# Running the Project

Run:

```bash
python main.py
```

The GUI launcher will open.

---

# How to Use

## Step 1

Enter:

- Student Name
- Roll Number

---

## Step 2

Click:

```text
Start Monitoring
```

---

## Step 3

Monitoring begins automatically.

The system will:

- monitor webcam
- detect suspicious activity
- send Telegram alerts
- save evidence images

---

# Telegram Commands

## /evidence

Shows saved evidence for current monitored student.

Evidence categories:

- Left Camera
- Multiple People
- Suspicious Activity

---

# Evidence Storage

Evidence images are stored inside:

```text
evidence/
```

Each student gets separate folder automatically.

Example:

```text
evidence/
└── 101_John/
    ├── left_camera.jpg
    ├── multiple_people.jpg
    └── suspicious_movement.jpg
```

---

# Building EXE

To build standalone executable:

```bash
pyinstaller --onefile --windowed --name Invigil --icon=assets/invigil.ico --add-data "assets;assets" --collect-data mediapipe --hidden-import mediapipe.python.solutions --hidden-import mediapipe.python.solutions.face_mesh --hidden-import mediapipe.python.solutions.drawing_utils main.py
```

Generated EXE will appear inside:

```text
dist/
```

---

# Important Notes

- Webcam permission must be enabled
- Internet connection required for Telegram alerts
- `.env` file should never be uploaded publicly
- Large EXE size is normal because MediaPipe and OpenCV are bundled

---

# Common Issues

## Telegram Not Working

Check:

- BOT_TOKEN correct
- CHAT_ID correct
- internet connection active

---

## Webcam Not Opening

Check:

- webcam connected
- camera permissions enabled
- no other application using webcam

---

## EXE Not Starting

Try:

- running as administrator
- temporarily disabling antivirus
- rebuilding executable

---

# Security Note

This project is intended for:

- educational purposes
- learning computer vision
- exam monitoring experimentation

Use responsibly and ethically.

---

# Future Improvements

Possible future upgrades:

- better head pose estimation
- session logging
- fullscreen exam lock
- database integration
- settings panel

---

# Developer

Developed by:

GeekSho

---
