import cv2
import os

# EVIDENCE FOLDER

os.makedirs(
    "evidence",
    exist_ok=True
)

# SAVE EVIDENCE

def save_evidence(
    frame,
    event_type,
    student_id
):

    try:

        student_folder = (
            f"evidence/{student_id}"
        )

        os.makedirs(
            student_folder,
            exist_ok=True
        )

        filepath = (
            f"{student_folder}/"
            f"{event_type}.jpg"
        )

        cv2.imwrite(
            filepath,
            frame
        )

        print(
            f"Evidence saved: {filepath}"
        )

    except Exception as e:

        print(
            "Evidence error:",
            e
        )