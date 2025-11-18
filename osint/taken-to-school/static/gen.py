import random
import hashlib
import ipaddress
from datetime import datetime, timedelta

NUMBER_LINES = 500

inject_line_num = random.randint(50, NUMBER_LINES-50)

# Constants
vendors = ["PaloAltoNetworks", "Gigamon"]
products = {
    "PaloAltoNetworks": "PAN-OS",
    "Gigamon": "GigaVUE"
}
events_login = ["Network Logon Attempt", "Remote Desktop Logon"]
events_threat = ["Spam Rule Matched", "Suspicious File Download", "Trojan Signature Match", "Ransomware Signature Match"]
file_names = [
    "math_homework_12.pdf", "biology_lab_report.docx", "class_roster.xlsx", "school_calendar_2024.pdf", "lecture_notes_week3.txt",
    "science_fair_poster.pptx", "student_grades_q1.xlsx", "syllabus_history101.pdf", "teacher_schedule.csv", "midterm_study_guide.docx",
    "attendance_log_march.csv", "chemistry_notes.pdf", "final_project_outline.docx", "exam_schedule_2024.pdf", "library_books_list.xlsx",
    "parent_letter_april.docx", "club_meeting_minutes.txt", "physics_equations_sheet.pdf", "gradebook_backup.xlsx", "field_trip_form.pdf",
    "course_materials.zip", "classroom_rules.docx", "student_feedback_form.docx", "essay_instructions.pdf", "sports_team_roster.xlsx",
    "school_logo.png", "cafeteria_menu_april.pdf", "it_helpdesk_requests.csv", "digital_citizenship_guide.pdf", "language_quiz_answers.docx"
]

threat_types = ["trojan", "worm", "spyware", "adware", "ransomware"]
usernames = [
    "admin", "jsmith", "mjones", "teacher.liu", "student.kpatel",
    "it.support", "registrar.office", "libtech1", "cafeteria.staff", "nurse.rwhite",
    "counselor.brooks", "vp_academics", "dean.morales", "student.ajackson", "prof.tnguyen",
    "substitute.mlewis", "coach.harris", "student2024.abrown", "student2025.singh", "teacher.egarcia",
    "techlab.intern", "hr.recruitment", "student.lwilliams", "ta.bkim", "math.dept",
    "history.faculty", "science.aadams", "student_user01", "librarian.jyoung", "helpdesk"
]

passwords = [
    "Winter2024!", "SpringBreak23", "MathRocks#1", "Science_2024", "Passw0rd2024",
    "Edu2024$", "SummerFun99!", "HistoryBuff#12", "Football!23", "GradeA2024",
    "SchoolTime#1", "BookLover2024", "Learn@Home1", "StudyHard!23", "Class12345!",
    "Teacher#2024", "LabReport#9", "CampusLife99", "QuizMaster_1", "ExamReady2024!",
    "Library$2023", "Campus123!", "Tut0r!ng4U", "ProjectX2024", "HelpDesk#1",
    "Football#23", "Coach@2024", "ScienceLab_1", "Student#2024", "Principal!9"
]

# protocols = ["TCP", "UDP", "ICMP"]
fixed_date = datetime(2024, 12, 22)

# Helper functions
def generate_md5():
    return hashlib.md5(str(random.random()).encode()).hexdigest()

def generate_public_ip():
    while True:
        ip = ipaddress.IPv4Address(random.randint(0x01000000, 0xEFFFFFFF))
        if not (ip.is_private or ip.is_loopback or ip.is_multicast or ip.is_reserved or ip.is_link_local):
            return str(ip)
        
def generate_private_ip():
    return f"192.168.11{random.randint(0, 9)}.{random.randint(1, 254)}"

# Generate entries
entries = []
for _ in range(500):

    timestamp = (fixed_date + timedelta(seconds=random.randint(0, 86399))).isoformat()
    version = f"{random.randint(8, 10)}.{random.randint(0, 9)}"
    signature_id = str(random.randint(10000, 99999))
    severity = random.randint(4, 10)
    action = random.choice(["detected", "quarantined", "blocked", "failed", "allowed"])
    src_ip = generate_public_ip()
    dst_ip = generate_private_ip()
    spt = random.randint(1024, 65535)
    md5_hash = generate_md5()

    

    if random.random() < 0.4 and not _ == inject_line_num:
        # Login attempt
        vendor = vendors[1]
        product = products[vendor]
        event = random.choice(events_login)
        if('Remote' in event):
            proto = 'TCP'
            dpt = '3389'
        else:
            proto = 'SMB'
            dpt = '445'
        user = random.choice(usernames)
        passwd = random.choice(passwords)
        cef = (f"{timestamp} CEF:0|{vendor}|{product}|{version}|{signature_id}|{event}|{severity}|"
               f"src={src_ip} dst={dst_ip} spt={spt} dpt={dpt} proto={proto} act={action} "
               f"cs1Label=username cs1={user} cs2Label=password cs2={passwd} eventHash={md5_hash}")
    else:
        # Threat event
        vendor = vendors[0]
        product = products[vendor]
        dpt = '443'
        proto = 'HTTPS'
        event = random.choice(events_threat)
        file = random.choice(file_names)
        threat = random.choice(threat_types)
        cef = (f"{timestamp} CEF:0|{vendor}|{product}|{version}|{signature_id}|{event}|{severity}|"
               f"src={src_ip} dst={dst_ip} spt={spt} dpt={dpt} proto={proto} act={action} "
               f"fileName={file} eventHash={md5_hash}")

        if(random.random() < 0.3):
            cef = (f"{timestamp} CEF:0|{vendor}|{product}|{version}|{signature_id}|{event}|{severity}|"
               f"src={src_ip} dst={dst_ip} spt={spt} dpt={dpt} proto={proto} act={action} "
               f"fileName={file} eventHash={md5_hash} cs1Label=threatType cs1={threat}")


    if _ == inject_line_num:
        src_ip = '91.218.50.11'
        event = 'Trojan Signature Match'
        action = 'allowed'
        cef = (f"{timestamp} CEF:0|{vendor}|{product}|{version}|{signature_id}|{event}|{severity}|"
               f"src={src_ip} dst={dst_ip} spt={spt} dpt={dpt} proto={proto} act={action} "
               f"fileName={file} eventHash={md5_hash} cs1Label=threatType cs1={threat}")

    entries.append(cef)

# Save to file
with open("generated_cef_md5_log_limited_sources.txt", "w") as f:
    for entry in entries:
        f.write(entry + "\n")

print("Log file generated: generated_cef_md5_log_limited_sources.txt")
