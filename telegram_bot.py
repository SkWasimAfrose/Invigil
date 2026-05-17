import requests
import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler
)

from config import *

selected_student = {}
current_live_student = ""

telegram_started = False

def set_current_student(
    student_id
):

    global current_live_student

    current_live_student = student_id

# TELEGRAM ALERT

def send_telegram_alert(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        if response.status_code != 200:

            print(
                "Telegram failed:",
                response.text
            )

    except Exception as e:

        print(
            "Telegram error:",
            e
        )

# SEND PHOTO

def send_telegram_photo(
    photo_path,
    caption
):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendPhoto"
    )

    try:

        with open(
            photo_path,
            "rb"
        ) as photo:

            files = {
                "photo": photo
            }

            data = {
                "chat_id": CHAT_ID,
                "caption": caption
            }

            response = requests.post(
                url,
                files=files,
                data=data,
                timeout=10
            )

            if response.status_code != 200:

                print(
                    "Photo failed:",
                    response.text
                )

    except Exception as e:

        print(
            "Photo error:",
            e
        )

# EVIDENCE COMMAND

def evidence_command(
    update,
    context
):

    student_buttons = []

    if current_live_student:

        student_buttons.append(
            [
                InlineKeyboardButton(
                    current_live_student,
                    callback_data=
                    f"student|{current_live_student}"
                )
            ]
        )

    if not student_buttons:

        update.message.reply_text(
            "No active monitoring session"
        )

        return
    
    keyboard = InlineKeyboardMarkup(
        student_buttons
    )

    update.message.reply_text(
        "Select Student",
        reply_markup=keyboard
    )

# BUTTON HANDLER

def button_handler(
    update,
    context
):

    query = update.callback_query

    query.answer()

    callback_data = query.data
    
    # STUDENT SELECTED

    if callback_data.startswith(
        "student|"
    ):

        student = (
            callback_data.split("|")[1]
        )

        selected_student[
            query.message.chat_id
        ] = student

        keyboard = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "Left Camera",
                    callback_data=
                    "event|left_camera"
                )
            ],

            [
                InlineKeyboardButton(
                    "Multiple People",
                    callback_data=
                    "event|multiple_people"
                )
            ],

            [
                InlineKeyboardButton(
                    "Suspicious Activity",
                    callback_data=
                    "event|suspicious_movement"
                )
            ]
        ])

        query.message.reply_text(
            f"Selected: {student}\n\nChoose Evidence Type",
            reply_markup=keyboard
        )
    
    # EVENT SELECTED

    elif callback_data.startswith(
        "event|"
    ):

        event = (
            callback_data.split("|")[1]
        )

        student = selected_student.get(
            query.message.chat_id
        )

        if student:

            photo_path = (
                f"evidence/"
                f"{student}/"
                f"{event}.jpg"
            )

            if os.path.exists(
                photo_path
            ):

                send_telegram_photo(
                    photo_path,
                    f"{student} - {event}"
                )

            else:

                send_telegram_alert(
                    "Evidence not found"
                )

# START TELEGRAM BOT

telegram_updater = None

def start_telegram_bot():
    global telegram_started

    if telegram_started:

       return

    telegram_started = True

    global telegram_updater

    telegram_updater = Updater(
        BOT_TOKEN,
        use_context=True
    )

    dispatcher = telegram_updater.dispatcher

    dispatcher.add_handler(
        CommandHandler(
            "evidence",
            evidence_command
        )
    )

    dispatcher.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    telegram_updater.start_polling()

    return telegram_updater

# STOP TELEGRAM BOT

def stop_telegram_bot():

    global telegram_updater

    if telegram_updater:

        telegram_updater.stop()

        telegram_updater.is_idle = False