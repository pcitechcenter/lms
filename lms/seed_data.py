"""
Frappe Bench Data Seeder
========================
Seeds sample data for: Users, LMS, and Education modules.

Usage:
    bench --site <site> execute lms.seed_data.seed_all
    bench --site <site> execute lms.seed_data.delete_all

Individual sections:
    bench --site <site> execute lms.seed_data.seed_users
    bench --site <site> execute lms.seed_data.seed_lms
    bench --site <site> execute lms.seed_data.seed_education
    bench --site <site> execute lms.seed_data.delete_users
    bench --site <site> execute lms.seed_data.delete_lms
    bench --site <site> execute lms.seed_data.delete_education

Via console (alternative):
    import importlib; m = importlib.import_module("lms.seed_data"); m.seed_all()
"""

import frappe
from frappe.utils import today, add_days


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _exists(doctype, filters):
    return frappe.db.exists(doctype, filters)


def _log(msg):
    print(f"  → {msg}")


def _delete_doc(doctype, name):
    try:
        doc = frappe.get_doc(doctype, name)
        if getattr(doc, "docstatus", 0) == 1:
            doc.cancel()
        frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)
        _log(f"deleted  {doctype} '{name}'")
    except Exception as e:
        _log(f"warn     could not delete {doctype} '{name}': {e}")


# ---------------------------------------------------------------------------
# 1. USERS
# ---------------------------------------------------------------------------

# NOTE: Dev/seed passwords only — change before production.
USERS = [
    # Instructors
    {
        "email": "maria.santos@educat.local",
        "first_name": "Maria",
        "last_name": "Santos",
        "username": "maria.santos",
        "user_type": "System User",
        "new_password": "Test@12345",
        "roles": ["Instructor", "Course Creator", "Academics User"],
    },
    {
        "email": "jose.reyes@educat.local",
        "first_name": "Jose",
        "last_name": "Reyes",
        "username": "jose.reyes",
        "user_type": "System User",
        "new_password": "Test@12345",
        "roles": ["Instructor", "Course Creator", "Academics User"],
    },
    # Students
    {
        "email": "juan.delacruz@educat.local",
        "first_name": "Juan",
        "last_name": "dela Cruz",
        "username": "juan.delacruz",
        "user_type": "Website User",
        "new_password": "Test@12345",
        "roles": ["Student", "LMS Student"],
    },
    {
        "email": "ana.bautista@educat.local",
        "first_name": "Ana",
        "last_name": "Bautista",
        "username": "ana.bautista",
        "user_type": "Website User",
        "new_password": "Test@12345",
        "roles": ["Student", "LMS Student"],
    },
    {
        "email": "miguel.ocampo@educat.local",
        "first_name": "Miguel",
        "last_name": "Ocampo",
        "username": "miguel.ocampo",
        "user_type": "Website User",
        "new_password": "Test@12345",
        "roles": ["Student", "LMS Student"],
    },
    {
        "email": "kristine.mendoza@educat.local",
        "first_name": "Kristine",
        "last_name": "Mendoza",
        "username": "kristine.mendoza",
        "user_type": "Website User",
        "new_password": "Test@12345",
        "roles": ["Student", "LMS Student"],
    },
    {
        "email": "marco.villanueva@educat.local",
        "first_name": "Marco",
        "last_name": "Villanueva",
        "username": "marco.villanueva",
        "user_type": "Website User",
        "new_password": "Test@12345",
        "roles": ["Student", "LMS Student"],
    },
    # Platform Administrator
    {
        "email": "rosario.garcia@educat.local",
        "first_name": "Rosario",
        "last_name": "Garcia",
        "username": "rosario.garcia",
        "user_type": "System User",
        "new_password": "Test@12345",
        "roles": ["Moderator", "System Manager", "Academics User"],
    },
]


def seed_users():
    print("\n[Users]")
    created = 0
    for u in USERS:
        if _exists("User", {"email": u["email"]}):
            _log(f"skip  {u['email']} (exists)")
            continue

        roles    = u.get("roles", [])
        password = u.get("new_password")
        fields   = {k: v for k, v in u.items() if k not in ("roles", "new_password")}

        doc = frappe.get_doc({"doctype": "User", "send_welcome_email": 0, "enabled": 1, **fields})

        for role in roles:
            if frappe.db.exists("Role", role):
                doc.append("roles", {"role": role})
            else:
                _log(f"  warn  role '{role}' not found — skipped")

        doc.insert(ignore_permissions=True)

        if password:
            from frappe.utils.password import update_password
            update_password(doc.name, password)

        _log(f"created  {doc.email} (password set)")
        created += 1

    frappe.db.commit()
    print(f"  Done — {created} new users created.")


def delete_users():
    print("\n[Delete — Users]")
    for u in USERS:
        if frappe.db.exists("User", u["email"]):
            _delete_doc("User", u["email"])
    frappe.db.commit()
    print("  Users deletion complete.")


# ---------------------------------------------------------------------------
# 2. LMS
# ---------------------------------------------------------------------------

LMS_COURSES = [
    {
        "title": "Panimula sa Python Programming",
        "short_introduction": "Matuto ng Python mula sa simula gamit ang mga praktikal na halimbawa.",
        "description": "<p>Isang kurso para sa mga baguhan na sumasaklaw sa Python syntax, istruktura ng datos, mga function, at OOP. Lahat ng halimbawa ay may kaugnayan sa pang-araw-araw na buhay sa Pilipinas.</p>",
        "category_name": "Programming",
        "instructor_email": "maria.santos@educat.local",
        "chapters": [
            {
                "title": "Pagsisimula sa Python",
                "lessons": [
                    {
                        "title": "Pag-install ng Python at Pag-setup",
                        "body": "## I-setup ang Python\n\nI-download ang Python 3.x mula sa python.org.\n\n```bash\npython --version\n```",
                        "include_in_preview": 1,
                    },
                    {
                        "title": "Mga Variable at Uri ng Datos",
                        "body": "## Mga Variable\n\n```python\npangalan = 'Juan dela Cruz'\nedad = 20\ngrado = 89.5\nmula_maynila = True\n```",
                    },
                    {
                        "title": "Control Flow: if/else at mga Loop",
                        "body": "## Kondisyon at Loop\n\n```python\nmga_rehiyon = ['NCR', 'Cebu', 'Davao', 'Iloilo']\nfor rehiyon in mga_rehiyon:\n    if rehiyon == 'NCR':\n        print(f'{rehiyon} — Kabisera')\n    else:\n        print(f'{rehiyon} — Probinsya')\n```",
                    },
                ],
            },
            {
                "title": "Mga Function at Module",
                "lessons": [
                    {
                        "title": "Pagsulat ng mga Function",
                        "body": "## Mga Function\n\n```python\ndef kumusta(pangalan: str) -> str:\n    return f'Kumusta, {pangalan}!'\n\nprint(kumusta('Maria Santos'))\n```",
                    },
                    {
                        "title": "Paggamit ng mga Module",
                        "body": "## Mga Built-in Module\n\n```python\nimport math\nimport random\n\nprint(math.pi)\nprint(random.randint(1, 100))\n```",
                    },
                ],
            },
            {
                "title": "Object-Oriented Programming",
                "lessons": [
                    {
                        "title": "Klase at Bagay (Classes and Objects)",
                        "body": "## OOP sa Python\n\n```python\nclass Mag_aaral:\n    def __init__(self, pangalan, numero):\n        self.pangalan = pangalan\n        self.numero = numero\n\n    def ipakita(self):\n        print(f'Estudyante: {self.pangalan}, No. {self.numero}')\n\nsi_juan = Mag_aaral('Juan dela Cruz', '2024-00123')\nsi_juan.ipakita()\n```",
                    },
                ],
            },
        ],
        "quiz": {
            "title": "Python Basics Quiz",
            "passing_percentage": 60,
            "questions": [
                {
                    "question": "Ano ang output ng print(type(42))?",
                    "type": "Choices",
                    "option_1": "<class 'int'>",   "is_correct_1": 1,
                    "option_2": "<class 'str'>",   "is_correct_2": 0,
                    "option_3": "<class 'float'>", "is_correct_3": 0,
                    "option_4": "<class 'num'>",   "is_correct_4": 0,
                },
                {
                    "question": "Anong keyword ang ginagamit para tukuyin ang isang function sa Python?",
                    "type": "Choices",
                    "option_1": "def",      "is_correct_1": 1,
                    "option_2": "function", "is_correct_2": 0,
                    "option_3": "fun",      "is_correct_3": 0,
                    "option_4": "fn",       "is_correct_4": 0,
                },
                {
                    "question": "Gumagamit ang Python ng indentation para tukuyin ang mga code block.",
                    "type": "Choices",
                    "option_1": "Tama",          "is_correct_1": 1,
                    "option_2": "Mali",          "is_correct_2": 0,
                    "option_3": "Minsan",        "is_correct_3": 0,
                    "option_4": "Sa loop lamang","is_correct_4": 0,
                },
            ],
        },
    },
    {
        "title": "Web Development gamit ang HTML at CSS",
        "short_introduction": "Gumawa ng modernong website mula sa simula.",
        "description": "<p>Alamin ang mga pundasyon ng web development — HTML na estruktura, CSS na istilo, Flexbox, at responsive design para sa mga Pilipinong web developer.</p>",
        "category_name": "Web Development",
        "instructor_email": "jose.reyes@educat.local",
        "chapters": [
            {
                "title": "Mga Pundasyon ng HTML",
                "lessons": [
                    {
                        "title": "Estruktura ng HTML Document",
                        "body": "## HTML Boilerplate\n\n```html\n<!DOCTYPE html>\n<html lang='fil'>\n  <head>\n    <meta charset='UTF-8'>\n    <title>Aking Pahina</title>\n  </head>\n  <body>\n    <h1>Mabuhay!</h1>\n  </body>\n</html>\n```",
                        "include_in_preview": 1,
                    },
                    {
                        "title": "Mga Karaniwang HTML Tag",
                        "body": "## Mga Tag\n\n- `<h1>`–`<h6>` — mga pamagat\n- `<p>` — talata\n- `<a href=''>` — link\n- `<img src='' alt=''>` — larawan\n- `<ul>` / `<ol>` — listahan",
                    },
                ],
            },
            {
                "title": "CSS at Disenyo",
                "lessons": [
                    {
                        "title": "Mga Selector at Property",
                        "body": "## CSS Basics\n\n```css\nbody {\n  font-family: 'Arial', sans-serif;\n  background-color: #f0f4f8;\n}\nh1 {\n  color: #0038a8; /* asul ng Pilipinas */\n}\n```",
                    },
                    {
                        "title": "Flexbox na Layout",
                        "body": "## Flexbox\n\n```css\n.lalagyan {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  gap: 1rem;\n}\n```",
                    },
                ],
            },
        ],
        "quiz": {
            "title": "HTML at CSS Quiz",
            "passing_percentage": 60,
            "questions": [
                {
                    "question": "Ano ang ibig sabihin ng HTML?",
                    "type": "Choices",
                    "option_1": "HyperText Markup Language",     "is_correct_1": 1,
                    "option_2": "High Text Machine Language",    "is_correct_2": 0,
                    "option_3": "HyperText Machine Language",    "is_correct_3": 0,
                    "option_4": "HyperTransfer Markup Language", "is_correct_4": 0,
                },
                {
                    "question": "Anong CSS property ang nagkokontrol sa kulay ng teksto?",
                    "type": "Choices",
                    "option_1": "color",            "is_correct_1": 1,
                    "option_2": "text-color",       "is_correct_2": 0,
                    "option_3": "font-color",       "is_correct_3": 0,
                    "option_4": "foreground-color", "is_correct_4": 0,
                },
            ],
        },
    },
    {
        "title": "Pagsusuri ng Datos gamit ang Pandas",
        "short_introduction": "Manipulahin at suriin ang datos gamit ang Pandas library ng Python.",
        "description": "<p>Sinasaklaw ang DataFrame, paglilinis ng datos, paggrugrupo, at basic na visualisasyon gamit ang datos mula sa kontekstong Pilipino.</p>",
        "category_name": "Data Science",
        "instructor_email": "maria.santos@educat.local",
        "chapters": [
            {
                "title": "Mga Pundasyon ng Pandas",
                "lessons": [
                    {
                        "title": "Paggawa ng DataFrame",
                        "body": "## DataFrame\n\n```python\nimport pandas as pd\n\ndf = pd.DataFrame({\n    'pangalan': ['Juan dela Cruz', 'Ana Bautista', 'Miguel Ocampo'],\n    'rehiyon':  ['NCR', 'Cebu', 'Davao'],\n    'grado':    [88, 92, 85]\n})\nprint(df)\n```",
                        "include_in_preview": 1,
                    },
                    {
                        "title": "Pagbabasa ng CSV Files",
                        "body": "## Basahin ang CSV\n\n```python\ndf = pd.read_csv('mga_estudyante.csv')\ndf.head()\ndf.info()\ndf.describe()\n```",
                    },
                ],
            },
            {
                "title": "Paglilinis ng Datos",
                "lessons": [
                    {
                        "title": "Pag-handle ng Nawawalang Halaga",
                        "body": "## Walang Datos (NaN)\n\n```python\ndf.dropna(inplace=True)\ndf['grado'].fillna(df['grado'].mean(), inplace=True)\nprint(df.isnull().sum())\n```",
                    },
                ],
            },
        ],
        "quiz": {
            "title": "Pandas Basics Quiz",
            "passing_percentage": 60,
            "questions": [
                {
                    "question": "Anong method ang nagpapakita ng unang 5 row ng isang DataFrame?",
                    "type": "Choices",
                    "option_1": "df.head()",  "is_correct_1": 1,
                    "option_2": "df.first()", "is_correct_2": 0,
                    "option_3": "df.top()",   "is_correct_3": 0,
                    "option_4": "df.show()",  "is_correct_4": 0,
                },
                {
                    "question": "Anong method ang nag-aalis ng mga row na may missing values?",
                    "type": "Choices",
                    "option_1": "df.dropna()", "is_correct_1": 1,
                    "option_2": "df.remove()", "is_correct_2": 0,
                    "option_3": "df.clean()",  "is_correct_3": 0,
                    "option_4": "df.delete()", "is_correct_4": 0,
                },
            ],
        },
    },
]

LMS_BATCHES = [
    {
        "title": "Python Bootcamp — Batch 2026-A (Maynila)",
        "start_date": today(),
        "end_date": add_days(today(), 60),
        "start_time": "09:00:00",
        "end_time": "11:00:00",
        "timezone": "Asia/Manila",
        "description": "Intensibong Python programming bootcamp para sa mga baguhan.",
        "batch_details": "<p>Live na sesyon tuwing Lunes at Miyerkules, 9–11 AM PHT.</p>",
        "instructor_email": "maria.santos@educat.local",
        "course_titles": ["Panimula sa Python Programming"],
    },
    {
        "title": "Web Dev Cohort — Unang Semestre 2026 (Cebu)",
        "start_date": add_days(today(), 14),
        "end_date": add_days(today(), 90),
        "start_time": "14:00:00",
        "end_time": "16:00:00",
        "timezone": "Asia/Manila",
        "description": "Matuto ng HTML at CSS at gumawa ng iyong unang responsive na website.",
        "batch_details": "<p>Biyernes, 2–4 PM PHT. May project review tuwing dalawang linggo.</p>",
        "instructor_email": "jose.reyes@educat.local",
        "course_titles": ["Web Development gamit ang HTML at CSS"],
    },
]


def _ensure_lms_category(name):
    if not name:
        return None
    if _exists("LMS Category", {"name": name}):
        return name
    try:
        doc = frappe.get_doc({"doctype": "LMS Category", "name": name, "category_name": name})
        doc.insert(ignore_permissions=True)
        return doc.name
    except Exception:
        return None


def _create_lms_question(q):
    existing = frappe.db.get_value("LMS Question", {"question": q["question"]}, "name")
    if existing:
        return existing
    doc = frappe.get_doc({
        "doctype":    "LMS Question",
        "question":   q["question"],
        "type":       q["type"],
        "option_1":   q.get("option_1", ""),
        "is_correct_1": q.get("is_correct_1", 0),
        "option_2":   q.get("option_2", ""),
        "is_correct_2": q.get("is_correct_2", 0),
        "option_3":   q.get("option_3", ""),
        "is_correct_3": q.get("is_correct_3", 0),
        "option_4":   q.get("option_4", ""),
        "is_correct_4": q.get("is_correct_4", 0),
    })
    doc.insert(ignore_permissions=True)
    return doc.name


def _create_lms_quiz(quiz_data):
    existing = frappe.db.get_value("LMS Quiz", {"title": quiz_data["title"]}, "name")
    if existing:
        _log(f"  skip  quiz '{quiz_data['title']}' (exists)")
        return existing
    doc = frappe.get_doc({
        "doctype":            "LMS Quiz",
        "title":              quiz_data["title"],
        "passing_percentage": quiz_data["passing_percentage"],
        "max_attempts":       3,
        "show_answers":       1,
        "questions": [
            {"question": _create_lms_question(q), "marks": 1}
            for q in quiz_data.get("questions", [])
        ],
    })
    doc.insert(ignore_permissions=True)
    _log(f"  created quiz '{doc.title}'")
    return doc.name


def seed_lms():
    print("\n[LMS Courses]")
    course_name_map = {}

    for course_data in LMS_COURSES:
        title = course_data["title"]

        if _exists("LMS Course", {"title": title}):
            _log(f"skip  '{title}' (exists)")
            course_name_map[title] = frappe.db.get_value("LMS Course", {"title": title}, "name")
            continue

        # 1. Insert course
        course_doc = frappe.get_doc({
            "doctype":            "LMS Course",
            "title":              title,
            "short_introduction": course_data["short_introduction"],
            "description":        course_data["description"],
            "published":          1,
            "enable_certification": 1,
            "instructors":        [{"instructor": course_data["instructor_email"]}],
        })
        category = _ensure_lms_category(course_data.get("category_name"))
        if category:
            course_doc.category = category
        course_doc.insert(ignore_permissions=True)
        course_name = course_doc.name
        course_name_map[title] = course_name
        _log(f"created course '{title}' → {course_name}")

        # 2. Create chapters + lessons
        chapter_names = []
        for ch_data in course_data.get("chapters", []):

            # Insert chapter
            ch_doc = frappe.get_doc({
                "doctype": "Course Chapter",
                "title":   ch_data["title"],
                "course":  course_name,
            })
            ch_doc.insert(ignore_permissions=True)
            ch_name = ch_doc.name

            # Insert all lessons, collecting their names
            lesson_names = []
            for ls_data in ch_data.get("lessons", []):
                ls_doc = frappe.get_doc({
                    "doctype":          "Course Lesson",
                    "title":            ls_data["title"],
                    "chapter":          ch_name,
                    "body":             ls_data.get("body", ""),
                    "include_in_preview": ls_data.get("include_in_preview", 0),
                })
                ls_doc.insert(ignore_permissions=True)
                lesson_names.append(ls_doc.name)

            # Reload chapter fresh (background hooks may have changed its timestamp)
            ch_doc = frappe.get_doc("Course Chapter", ch_name)
            for ln in lesson_names:
                ch_doc.append("lessons", {"lesson": ln})
            ch_doc.save(ignore_permissions=True)
            chapter_names.append(ch_name)

        # 3. Reload course fresh and attach all chapters
        course_doc = frappe.get_doc("LMS Course", course_name)
        for ch in chapter_names:
            course_doc.append("chapters", {"chapter": ch})
        course_doc.save(ignore_permissions=True)

        # 4. Quiz
        quiz_data = course_data.get("quiz")
        quiz_name = _create_lms_quiz(quiz_data) if quiz_data else None
        _log(f"  {len(chapter_names)} chapters, quiz: {quiz_name or 'none'}")

    frappe.db.commit()

    # Batches
    print("\n[LMS Batches]")
    for batch_data in LMS_BATCHES:
        title = batch_data["title"]
        if _exists("LMS Batch", {"title": title}):
            _log(f"skip  '{title}' (exists)")
            continue

        batch_doc = frappe.get_doc({
            "doctype":      "LMS Batch",
            "title":        title,
            "start_date":   batch_data["start_date"],
            "end_date":     batch_data["end_date"],
            "start_time":   batch_data["start_time"],
            "end_time":     batch_data["end_time"],
            "timezone":     batch_data["timezone"],
            "description":  batch_data["description"],
            "batch_details": batch_data["batch_details"],
            "published":    1,
            "instructors":  [{"instructor": batch_data["instructor_email"]}],
            "courses": [
                {"course": course_name_map[ct], "title": ct}
                for ct in batch_data.get("course_titles", [])
                if ct in course_name_map
            ],
        })
        batch_doc.insert(ignore_permissions=True)
        _log(f"created batch '{title}'")

    frappe.db.commit()

    # Enrollments
    print("\n[LMS Enrollments]")
    student_emails = [u["email"] for u in USERS if "LMS Student" in u.get("roles", [])]
    for i, email in enumerate(student_emails):
        for j, cd in enumerate(LMS_COURSES):
            if (i + j) % 2 == 0:
                continue
            cn = course_name_map.get(cd["title"])
            if not cn:
                continue
            if _exists("LMS Enrollment", {"member": email, "course": cn}):
                _log(f"skip  enrollment {email} → {cn} (exists)")
                continue
            frappe.get_doc({
                "doctype":     "LMS Enrollment",
                "member":      email,
                "course":      cn,
                "member_type": "Student",
            }).insert(ignore_permissions=True)
            _log(f"enrolled  {email} → {cn}")

    frappe.db.commit()
    print("  LMS seeding complete.")


def delete_lms():
    print("\n[Delete — LMS Enrollments]")
    student_emails = [u["email"] for u in USERS if "LMS Student" in u.get("roles", [])]
    for email in student_emails:
        for name in frappe.get_all("LMS Enrollment", filters={"member": email}, pluck="name"):
            _delete_doc("LMS Enrollment", name)
        for name in frappe.get_all("LMS Batch Enrollment", filters={"member": email}, pluck="name"):
            _delete_doc("LMS Batch Enrollment", name)

    print("\n[Delete — LMS Batches]")
    for bd in LMS_BATCHES:
        name = frappe.db.get_value("LMS Batch", {"title": bd["title"]}, "name")
        if name:
            _delete_doc("LMS Batch", name)

    print("\n[Delete — LMS Courses]")
    for cd in LMS_COURSES:
        course_name = frappe.db.get_value("LMS Course", {"title": cd["title"]}, "name")
        if not course_name:
            _log(f"skip  '{cd['title']}' (not found)")
            continue

        # Quiz + questions
        quiz_data = cd.get("quiz")
        if quiz_data:
            quiz_name = frappe.db.get_value("LMS Quiz", {"title": quiz_data["title"]}, "name")
            if quiz_name:
                quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)
                for row in quiz_doc.questions:
                    _delete_doc("LMS Question", row.question)
                _delete_doc("LMS Quiz", quiz_name)

        # Lessons → chapters
        for ch_name in frappe.get_all("Course Chapter", filters={"course": course_name}, pluck="name"):
            ch_doc = frappe.get_doc("Course Chapter", ch_name)
            for ls_row in ch_doc.lessons:
                _delete_doc("Course Lesson", ls_row.lesson)
            _delete_doc("Course Chapter", ch_name)

        _delete_doc("LMS Course", course_name)

    frappe.db.commit()
    print("  LMS deletion complete.")


# ---------------------------------------------------------------------------
# 3. EDUCATION
# ---------------------------------------------------------------------------

ACADEMIC_YEAR_NAME = "A.Y. 2025-2026"
ACADEMIC_TERMS = [
    {
        "term_name":       "1st Semester",
        "term_start_date": "2025-08-01",
        "term_end_date":   "2025-12-20",
    },
    {
        "term_name":       "2nd Semester",
        "term_start_date": "2026-01-05",
        "term_end_date":   "2026-05-31",
    },
]

EDU_PROGRAMS = [
    {
        "program_name":         "Bachelor of Science in Computer Science",
        "program_abbreviation": "BSCS",
        "courses": [
            "Data Structures and Algorithms",
            "Database Management Systems",
            "Operating Systems",
            "Software Engineering",
        ],
    },
    {
        "program_name":         "Bachelor of Science in Information Technology",
        "program_abbreviation": "BSIT",
        "courses": [
            "Web Systems and Technologies",
            "Database Management Systems",
            "Systems Analysis and Design",
            "ICT Project Management",
        ],
    },
]

EDU_COURSES = [
    {"course_name": "Data Structures and Algorithms",  "description": "Mga istruktura ng datos at disenyo ng algorithm kasama ang complexity analysis."},
    {"course_name": "Database Management Systems",     "description": "Relational na database, SQL, normalisasyon, indexing, at transaksyon gamit ang MariaDB."},
    {"course_name": "Operating Systems",               "description": "Process management, memory management, file system, at seguridad ng OS."},
    {"course_name": "Software Engineering",            "description": "SDLC models, agile methodology, software testing, at project management."},
    {"course_name": "Web Systems and Technologies",    "description": "Pagbuo ng web application gamit ang HTML, CSS, JavaScript, at PHP/Laravel."},
    {"course_name": "Systems Analysis and Design",     "description": "Pagdidisenyo ng impormasyon sistemo gamit ang UML at structured methodologies."},
    {"course_name": "ICT Project Management",          "description": "Pamamahala ng ICT proyekto: scope, oras, gastos, kalidad, at risk management."},
]

INSTRUCTORS = [
    {"instructor_name": "Maria Santos", "email": "maria.santos@educat.local"},
    {"instructor_name": "Jose Reyes",   "email": "jose.reyes@educat.local"},
]

STUDENTS = [
    {"first_name": "Juan",     "last_name": "dela Cruz",  "student_email_id": "juan.delacruz@educat.local"},
    {"first_name": "Ana",      "last_name": "Bautista",   "student_email_id": "ana.bautista@educat.local"},
    {"first_name": "Miguel",   "last_name": "Ocampo",     "student_email_id": "miguel.ocampo@educat.local"},
    {"first_name": "Kristine", "last_name": "Mendoza",    "student_email_id": "kristine.mendoza@educat.local"},
    {"first_name": "Marco",    "last_name": "Villanueva", "student_email_id": "marco.villanueva@educat.local"},
]


def seed_education():
    # Academic Year
    print("\n[Education — Academic Year & Terms]")
    if not _exists("Academic Year", {"academic_year_name": ACADEMIC_YEAR_NAME}):
        frappe.get_doc({
            "doctype":            "Academic Year",
            "academic_year_name": ACADEMIC_YEAR_NAME,
            "year_start_date":    "2025-08-01",
            "year_end_date":      "2026-05-31",
        }).insert(ignore_permissions=True)
        _log(f"created academic year '{ACADEMIC_YEAR_NAME}'")
    else:
        _log(f"skip  academic year '{ACADEMIC_YEAR_NAME}' (exists)")

    # Academic Terms
    term_name_map = {}
    for t in ACADEMIC_TERMS:
        existing = frappe.db.exists("Academic Term", {
            "academic_year": ACADEMIC_YEAR_NAME,
            "term_name":     t["term_name"],
        })
        if existing:
            _log(f"skip  term '{t['term_name']}' (exists)")
            term_name_map[t["term_name"]] = existing
        else:
            doc = frappe.get_doc({
                "doctype":         "Academic Term",
                "academic_year":   ACADEMIC_YEAR_NAME,
                "term_name":       t["term_name"],
                "term_start_date": t["term_start_date"],
                "term_end_date":   t["term_end_date"],
            })
            doc.insert(ignore_permissions=True)
            term_name_map[t["term_name"]] = doc.name
            _log(f"created term '{doc.name}'")

    # Courses
    print("\n[Education — Courses]")
    course_name_map = {}
    for c in EDU_COURSES:
        if _exists("Course", {"course_name": c["course_name"]}):
            _log(f"skip  '{c['course_name']}' (exists)")
            course_name_map[c["course_name"]] = c["course_name"]
            continue
        doc = frappe.get_doc({
            "doctype":     "Course",
            "course_name": c["course_name"],
            "description": c.get("description", ""),
        })
        doc.insert(ignore_permissions=True)
        course_name_map[c["course_name"]] = doc.name
        _log(f"created course '{doc.name}'")

    # Programs
    print("\n[Education — Programs]")
    program_name_map = {}
    for p in EDU_PROGRAMS:
        if _exists("Program", {"program_name": p["program_name"]}):
            _log(f"skip  '{p['program_name']}' (exists)")
            program_name_map[p["program_name"]] = p["program_name"]
            continue
        doc = frappe.get_doc({
            "doctype":              "Program",
            "program_name":         p["program_name"],
            "program_abbreviation": p.get("program_abbreviation", ""),
            "courses": [
                {"course": course_name_map[cn], "course_name": cn, "required": 1}
                for cn in p["courses"] if cn in course_name_map
            ],
        })
        doc.insert(ignore_permissions=True)
        program_name_map[p["program_name"]] = doc.name
        _log(f"created program '{doc.name}'")

    # Instructors
    print("\n[Education — Instructors]")
    for instr in INSTRUCTORS:
        if _exists("Instructor", {"instructor_name": instr["instructor_name"]}):
            _log(f"skip  '{instr['instructor_name']}' (exists)")
            continue
        frappe.get_doc({
            "doctype":         "Instructor",
            "instructor_name": instr["instructor_name"],
        }).insert(ignore_permissions=True)
        _log(f"created instructor '{instr['instructor_name']}'")

    # Students
    print("\n[Education — Students]")
    student_name_map = {}
    for s in STUDENTS:
        if _exists("Student", {"student_email_id": s["student_email_id"]}):
            _log(f"skip  '{s['first_name']} {s['last_name']}' (exists)")
            student_name_map[s["student_email_id"]] = frappe.db.get_value(
                "Student", {"student_email_id": s["student_email_id"]}, "name"
            )
            continue
        doc = frappe.get_doc({
            "doctype":          "Student",
            "first_name":       s["first_name"],
            "last_name":        s["last_name"],
            "student_email_id": s["student_email_id"],
            "joining_date":     today(),
            "enabled":          1,
        })
        doc.insert(ignore_permissions=True)
        student_name_map[s["student_email_id"]] = doc.name
        _log(f"created student '{doc.name}' ({s['student_email_id']})")

    # Student Groups
    print("\n[Education — Student Groups]")
    for p in EDU_PROGRAMS:
        prog_name  = program_name_map.get(p["program_name"])
        group_name = f"{p['program_abbreviation']} - {ACADEMIC_YEAR_NAME}"
        if not prog_name or _exists("Student Group", {"student_group_name": group_name}):
            _log(f"skip  group '{group_name}'")
            continue
        frappe.get_doc({
            "doctype":            "Student Group",
            "student_group_name": group_name,
            "academic_year":      ACADEMIC_YEAR_NAME,
            "academic_term":      term_name_map.get("1st Semester"),
            "group_based_on":     "Batch",
            "program":            prog_name,
            "students": [
                {"student": sn, "active": 1}
                for sn in student_name_map.values()
            ],
        }).insert(ignore_permissions=True)
        _log(f"created student group '{group_name}'")

    frappe.db.commit()

    # Program Enrollments
    print("\n[Education — Program Enrollments]")
    first_term = term_name_map.get("1st Semester")
    for i, s in enumerate(STUDENTS):
        student_name = student_name_map.get(s["student_email_id"])
        if not student_name:
            continue
        p         = EDU_PROGRAMS[i % len(EDU_PROGRAMS)]
        prog_name = program_name_map.get(p["program_name"])
        if not prog_name:
            continue
        if _exists("Program Enrollment", {
            "student":       student_name,
            "program":       prog_name,
            "academic_year": ACADEMIC_YEAR_NAME,
        }):
            _log(f"skip  enrollment {student_name} → {prog_name} (exists)")
            continue

        enr = frappe.get_doc({
            "doctype":        "Program Enrollment",
            "student":        student_name,
            "program":        prog_name,
            "academic_year":  ACADEMIC_YEAR_NAME,
            "academic_term":  first_term,
            "enrollment_date": today(),
            "courses": [
                {"course": course_name_map[cn], "course_name": cn}
                for cn in p["courses"] if cn in course_name_map
            ],
        })
        enr.insert(ignore_permissions=True)
        enr.submit()
        _log(f"enrolled  {student_name} → {prog_name} (submitted)")

    frappe.db.commit()
    print("  Education seeding complete.")


def delete_education():
    print("\n[Delete — Program Enrollments]")
    for s in STUDENTS:
        student_name = frappe.db.get_value(
            "Student", {"student_email_id": s["student_email_id"]}, "name"
        )
        if not student_name:
            continue
        for name in frappe.get_all("Program Enrollment", filters={"student": student_name}, pluck="name"):
            _delete_doc("Program Enrollment", name)

    print("\n[Delete — Student Groups]")
    for p in EDU_PROGRAMS:
        group_name = f"{p['program_abbreviation']} - {ACADEMIC_YEAR_NAME}"
        if frappe.db.exists("Student Group", group_name):
            _delete_doc("Student Group", group_name)

    print("\n[Delete — Students]")
    for s in STUDENTS:
        name = frappe.db.get_value("Student", {"student_email_id": s["student_email_id"]}, "name")
        if name:
            _delete_doc("Student", name)

    print("\n[Delete — Instructors]")
    for instr in INSTRUCTORS:
        name = frappe.db.get_value("Instructor", {"instructor_name": instr["instructor_name"]}, "name")
        if name:
            _delete_doc("Instructor", name)

    print("\n[Delete — Programs]")
    for p in EDU_PROGRAMS:
        if frappe.db.exists("Program", p["program_name"]):
            _delete_doc("Program", p["program_name"])

    print("\n[Delete — Education Courses]")
    for c in EDU_COURSES:
        if frappe.db.exists("Course", c["course_name"]):
            _delete_doc("Course", c["course_name"])

    print("\n[Delete — Academic Terms & Year]")
    for t in ACADEMIC_TERMS:
        name = frappe.db.get_value("Academic Term", {
            "academic_year": ACADEMIC_YEAR_NAME,
            "term_name":     t["term_name"],
        }, "name")
        if name:
            _delete_doc("Academic Term", name)
    if frappe.db.exists("Academic Year", ACADEMIC_YEAR_NAME):
        _delete_doc("Academic Year", ACADEMIC_YEAR_NAME)

    frappe.db.commit()
    print("  Education deletion complete.")


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def seed_all():
    print("=" * 60)
    print("  Frappe Bench — Data Seeder")
    print("=" * 60)
    seed_users()
    seed_lms()
    seed_education()
    frappe.db.commit()
    print("\n" + "=" * 60)
    print("  Seeding complete!")
    print("=" * 60)


def delete_all():
    print("=" * 60)
    print("  Frappe Bench — Deleting Seed Data")
    print("=" * 60)
    delete_lms()
    delete_education()
    delete_users()
    frappe.db.commit()
    print("\n" + "=" * 60)
    print("  Deletion complete!")
    print("=" * 60)
