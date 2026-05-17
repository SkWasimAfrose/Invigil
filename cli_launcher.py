from monitor import start_monitoring

# STUDENT LOGIN

student_name = input(
    "Enter Student Name: "
)

roll_number = input(
    "Enter Roll Number: "
)

STUDENT_ID = (
    f"{roll_number}_{student_name}"
)

start_monitoring(
    STUDENT_ID
)