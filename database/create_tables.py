import sqlite3
import random
from faker import Faker

"""
AI PROMPT
You are my boss and I'm your data analyst/engineer. Give me ONE task for practicing sql 
utilising the below database and tables. Do not give me the answer or any code I just 
want the task as if you are my stakeholder. I'm not yet in a data job and I'd probably say i'm mid (ish level)
I'm better than select from where, I can do CTE's and i'm practicing window functions and group by at the moment

These are what I have done already
find_countries_with_most_training_completions.sql
find_departments_with_poor_employee_stats.sql
find_highest_paid_employees.sql
find_performance_averages.sql
find_performance_averages_by_country.sql
find_top_absent_employees.sql
find_top_five_projects.sql
find_top_five_salaries.sql
find_top_five_training_completers.sql
find_top_two_departments_scores.sql
find_widest_performance_gap_for_departments.sql
find_worst_performing_departments.sql
salary_comparison.sql
salary_ranking.sql
training_coverage.sql
training_stats.sql

"""


def create_hr_database() -> None:
    fake = Faker()
    conn = sqlite3.connect("hr_database.db")
    cursor = conn.cursor()
    tables = [
        "employees",
        "departments",
        "jobs",
        "projects",
        "salaries",
        "attendance",
        "performance",
        "benefits",
        "training",
        "locations",
    ]
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t}")
    cursor.execute("""
    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location_id INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        country TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        hire_date TEXT,
        department_id INTEGER,
        job_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(department_id),
        FOREIGN KEY(job_id) REFERENCES jobs(job_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        min_salary REAL,
        max_salary REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date TEXT,
        end_date TEXT,
        department_id INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(department_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE salaries (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        amount REAL,
        effective_date TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        review_date TEXT,
        score INTEGER,
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE benefits (
        benefit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        benefit_type TEXT,
        start_date TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE training (
        training_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        course_name TEXT,
        completion_date TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
    )
    """)
    NUM_ROWS = 500
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO locations (city, country) VALUES (?, ?)",
            (fake.city(), fake.country()),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO departments (name, location_id) VALUES (?, ?)",
            (fake.job(), random.randint(1, NUM_ROWS)),
        )
    for _ in range(NUM_ROWS):
        min_salary = random.randint(30000, 50000)
        max_salary = min_salary + random.randint(10000, 50000)
        cursor.execute(
            "INSERT INTO jobs (title, min_salary, max_salary) VALUES (?, ?, ?)",
            (fake.job(), min_salary, max_salary),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            """
        INSERT INTO employees (first_name, last_name, email, phone, hire_date, department_id, job_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                fake.first_name(),
                fake.last_name(),
                fake.email(),
                fake.phone_number(),
                fake.date_between(start_date="-10y", end_date="today"),
                random.randint(1, NUM_ROWS),
                random.randint(1, NUM_ROWS),
            ),
        )
    for _ in range(NUM_ROWS):
        start_date = fake.date_between(start_date="-5y", end_date="-1y")
        end_date = fake.date_between(start_date="-1y", end_date="today")
        cursor.execute(
            "INSERT INTO projects (name, start_date, end_date, department_id) VALUES (?, ?, ?, ?)",
            (fake.bs(), start_date, end_date, random.randint(1, NUM_ROWS)),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO salaries (employee_id, amount, effective_date) VALUES (?, ?, ?)",
            (
                random.randint(1, NUM_ROWS),
                random.uniform(30000, 120000),
                fake.date_between(start_date="-5y", end_date="today"),
            ),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO attendance (employee_id, date, status) VALUES (?, ?, ?)",
            (
                random.randint(1, NUM_ROWS),
                fake.date_between(start_date="-1y", end_date="today"),
                random.choice(["Present", "Absent", "Remote"]),
            ),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO performance (employee_id, review_date, score) VALUES (?, ?, ?)",
            (
                random.randint(1, NUM_ROWS),
                fake.date_between(start_date="-2y", end_date="today"),
                random.randint(1, 5),
            ),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO benefits (employee_id, benefit_type, start_date) VALUES (?, ?, ?)",
            (
                random.randint(1, NUM_ROWS),
                random.choice(["Health", "Dental", "Vision", "Retirement"]),
                fake.date_between(start_date="-3y", end_date="today"),
            ),
        )
    for _ in range(NUM_ROWS):
        cursor.execute(
            "INSERT INTO training (employee_id, course_name, completion_date) VALUES (?, ?, ?)",
            (
                random.randint(1, NUM_ROWS),
                fake.catch_phrase(),
                fake.date_between(start_date="-2y", end_date="today"),
            ),
        )
    conn.commit()
    conn.close()

    print("HR database created with 10 tables and random data!")


def main() -> None:
    create_hr_database()


if __name__ == "__main__":
    main()
