import cv2
import mediapipe as mp
import time

monitoring_active = True
current_student_id = ""

from config import *
from telegram_bot import *
from evidence import *

cv2.setUseOptimized(True)

cv2.setNumThreads(4)

# START MONITORING

def start_monitoring(
    STUDENT_ID
):
    
    global current_student_id
    global monitoring_active

    monitoring_active = True

    current_student_id = STUDENT_ID
    
    # OPEN WEBCAM

    cap = cv2.VideoCapture(0)

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    if not cap.isOpened():

        print(
            "Error: Could not open webcam"
        )

        return

    print(
        "Online Exam Monitoring Started"
    )

    send_telegram_alert(
        f"✅ {STUDENT_ID} monitoring started"
    )
    
    # MEDIAPIPE SETUP

    mp_face_mesh = mp.solutions.face_mesh

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=MAX_FACES,
        refine_landmarks=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    mp_draw = mp.solutions.drawing_utils
    
    # VARIABLES

    suspicion_score = 0

    side_counter = 0

    frame_counter = 0

    last_score_time = 0

    last_decay_time = time.time()

    no_face_start_time = None
    
    # ALERT STATES

    multiple_face_active = False

    no_face_active = False

    suspicious_active = False

    face_count = 0
    
    # MAIN LOOP

    while monitoring_active:

        success, frame = cap.read()

        frame_counter += 1

        if frame_counter % FRAME_SKIP != 0:
            continue

        if not success:

            print(
                "Failed to grab frame"
            )

            break

        if DEBUG_MODE:

            frame = cv2.flip(
                frame,
                1
            )

        h, w, _ = frame.shape

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb)

        status = "NORMAL"

        current_time = time.time()
        
        # FACE DETECTION

        if results.multi_face_landmarks:

            face_count = len(
                results.multi_face_landmarks
            )

            if no_face_active:

                send_telegram_alert(
                    f"✅ {STUDENT_ID} returned to camera"
                )

                no_face_active = False

            no_face_start_time = None
            
            # MULTIPLE FACE

            if face_count > 1:

                status = (
                    "MULTIPLE PEOPLE DETECTED"
                )

                if not multiple_face_active:

                    send_telegram_alert(
                        f"⚠ {STUDENT_ID}: Multiple people detected"
                    )

                    save_evidence(
                        frame,
                        "multiple_people",
                        STUDENT_ID
                    )

                    multiple_face_active = True

            else:

                if multiple_face_active:

                    send_telegram_alert(
                        f"✅ {STUDENT_ID}: Multiple people issue resolved"
                    )

                    multiple_face_active = False
            
            # SINGLE FACE ANALYSIS

            face_landmarks = (
                results.multi_face_landmarks[0]
            )

            nose = (
                face_landmarks.landmark[1]
            )

            left_cheek = (
                face_landmarks.landmark[234]
            )

            right_cheek = (
                face_landmarks.landmark[454]
            )

            nose_x = int(nose.x * w)

            left_cheek_x = int(
                left_cheek.x * w
            )

            right_cheek_x = int(
                right_cheek.x * w
            )

            face_center_x = (
                left_cheek_x
                + right_cheek_x
            ) // 2

            horizontal_distance = (
                nose_x - face_center_x
            )
            
            # LEFT / RIGHT DETECTION

            if horizontal_distance < -45:

                status = "LOOKING LEFT"

                side_counter += 1

            elif horizontal_distance > 45:

                status = "LOOKING RIGHT"

                side_counter += 1

            else:

                side_counter = 0
            
            # SUSPICION SCORE

            if side_counter > 25:

                if (
                    current_time
                    - last_score_time
                    > SCORE_COOLDOWN
                ):

                    suspicion_score += 1

                    last_score_time = (
                        current_time
                    )

                    last_decay_time = (
                        current_time
                    )

                side_counter = 0
            
            # FINAL ALERT

            if (
                suspicion_score
                >= SUSPICION_THRESHOLD
            ):

                if not suspicious_active:

                    send_telegram_alert(
                        f"⚠ {STUDENT_ID}: Suspicious side movement detected"
                    )

                    save_evidence(
                        frame,
                        "suspicious_movement",
                        STUDENT_ID
                    )

                    suspicious_active = True

            else:

                if suspicious_active:

                    send_telegram_alert(
                        f"✅ {STUDENT_ID}: Suspicious activity normalized"
                    )

                    suspicious_active = False
            
            # DRAW LANDMARKS

            if DEBUG_MODE:

                for landmarks in (
                    results.multi_face_landmarks
                ):

                    mp_draw.draw_landmarks(
                        frame,
                        landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS
                    )

        else:

            face_count = 0

            status = "NO FACE DETECTED"

            if no_face_start_time is None:

                no_face_start_time = (
                    time.time()
                )

            no_face_duration = int(
                current_time
                - no_face_start_time
            )

            if (
                no_face_duration
                >= LEFT_CAMERA_TIME
            ):

                status = (
                    "STUDENT LEFT CAMERA"
                )

                if not no_face_active:

                    send_telegram_alert(
                        f"⚠ {STUDENT_ID} left camera"
                    )

                    save_evidence(
                        frame,
                        "left_camera",
                        STUDENT_ID
                    )

                    no_face_active = True
        
        # SCORE DECAY

        if status == "NORMAL":

            if (
                current_time
                - last_decay_time
                > 15
            ):

                if suspicion_score > 0:

                    suspicion_score -= 1

                last_decay_time = (
                    current_time
                )
        
        # DEBUG WINDOW

        if DEBUG_MODE:

            color = (0, 255, 0)

            if (
                "MULTIPLE" in status
                or "LEFT CAMERA" in status
            ):

                color = (0, 0, 255)

            elif (
                "LEFT" in status
                or "RIGHT" in status
            ):

                color = (0, 165, 255)

            cv2.putText(
                frame,
                f"Student: {STUDENT_ID}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Status: {status}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            cv2.putText(
                frame,
                f"Faces: {face_count}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Score: {suspicion_score}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "Online Exam Monitoring",
                frame
            )

            if (
                cv2.waitKey(1)
                & 0xFF
                == ord('q')
            ):

                break
    
    # CLEANUP

    cap.release()

    cv2.destroyAllWindows()

    face_mesh.close()

# STOP MONITORING

def stop_monitoring():

    global monitoring_active
    global current_student_id

    monitoring_active = False

    try:

        send_telegram_alert(
            f"⚠ {current_student_id} monitoring disconnected"
        )

    except Exception as e:

        print(
            "Disconnect alert error:",
            e
        )