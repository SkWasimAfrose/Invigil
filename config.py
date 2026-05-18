import os
import sys

from dotenv import load_dotenv

if getattr(sys, 'frozen', False):

    BASE_DIR = os.path.dirname(
        sys.executable
    )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

dotenv_path = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    dotenv_path
)

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "CHAT_ID"
)

# SYSTEM SETTINGS

DEBUG_MODE = False

FRAME_SKIP = 2

MAX_FACES = 2

LEFT_CAMERA_TIME = 10

SUSPICION_THRESHOLD = 5

SCORE_COOLDOWN = 2

# GUI SETTINGS

APP_TITLE = "Invigil"

WINDOW_WIDTH = 600

WINDOW_HEIGHT = 500