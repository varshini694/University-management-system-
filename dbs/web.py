import streamlit as st
import mysql.connector

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kavitha07@',
    'database': 'dbs'
}

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)

# Authenticate user and retrieve role
def authenticate_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, role_id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        user_id, role_id = user
        cursor.execute("SELECT role_name FROM roles WHERE role_id = %s", (role_id,))
        role_name = cursor.fetchone()[0]
        cursor.close()
        db.close()
        return user_id, role_name
    else:
        cursor.close()
        db.close()
        return None, None

# Functions to manage students and faculty
def view_students():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return students

def add_student(name, department, year, faculty_id):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO students (name, department, year, faculty_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, department, year, faculty_id))
    db.commit()
    cursor.close()
    db.close()

def update_student(student_id, new_name, new_department, new_year):
    db = connect_db()
    cursor = db.cursor()
    sql = "UPDATE students SET name = %s, department = %s, year = %s WHERE student_id = %s"
    cursor.execute(sql, (new_name, new_department, new_year, student_id))
    db.commit()
    cursor.close()
    db.close()

def delete_student(student_id):
    db = connect_db()
    cursor = db.cursor()
    sql = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(sql, (student_id,))
    db.commit()
    cursor.close()
    db.close()

def view_all_faculty():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM faculty")
    faculty_members = cursor.fetchall()
    cursor.close()
    db.close()
    return faculty_members

# Function to add a new faculty member
def add_faculty(name, department):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO faculty (name, department) VALUES (%s, %s)"
    cursor.execute(sql, (name, department))
    db.commit()
    cursor.close()
    db.close()

# Function to update a faculty member's details
def update_faculty(faculty_id, new_name, new_department):
    db = connect_db()
    cursor = db.cursor()
    sql = "UPDATE faculty SET name = %s, department = %s WHERE faculty_id = %s"
    cursor.execute(sql, (new_name, new_department, faculty_id))
    db.commit()
    cursor.close()
    db.close()

# Function to delete a faculty member
def delete_faculty(faculty_id):
    db = connect_db()
    cursor = db.cursor()
    sql = "DELETE FROM faculty WHERE faculty_id = %s"
    cursor.execute(sql, (faculty_id,))
    db.commit()
    cursor.close()
    db.close()


# Streamlit app
st.title("College Management System")

# Initialize session state
if 'role_name' not in st.session_state:
    st.session_state.role_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Login form
if st.session_state.role_name is None:
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    login_button = st.sidebar.button("Login")

    if login_button:
        user_id, role_name = authenticate_user(username, password)
        if role_name:
            st.session_state.role_name = role_name
            st.session_state.user_id = user_id
            st.success(f"Logged in as {role_name}")
        else:
            st.error("Invalid username or password.")

# Role-based functionality
if st.session_state.role_name:
    if st.session_state.role_name == 'Academic Advisor':
        st.header("Academic Advisor Dashboard")
        action = st.selectbox("Select Action", ["View Students", "Add Student", "Update Student", "Delete Student", "View Faculty", "Update Faculty"])
        
        if action == "View Students":
            students = view_students()
            for student in students:
                st.write(f"Student ID: {student[0]}, Name: {student[1]}, Department: {student[5]}, Year: {student[3]}")

        elif action == "Add Student":
            with st.form("Add Student Form"):
                name = st.text_input("Student Name")
                department = st.text_input("Department")
                year = st.number_input("Year", min_value=1)
                faculty_id = st.number_input("Faculty ID", min_value=1, format="%d")
                submit_button = st.form_submit_button("Add Student")
                if submit_button:
                    add_student(name, department, year, faculty_id)
                    st.success("Student added successfully.")

        elif action == "Update Student":
            with st.form("Update Student Form"):
                student_id = st.number_input("Student ID", min_value=1)
                new_name = st.text_input("New Student Name")
                new_department = st.text_input("New Department")
                new_year = st.number_input("New Year", min_value=1)
                submit_button = st.form_submit_button("Update Student")
                if submit_button:
                    update_student(student_id, new_name, new_department, new_year)
                    st.success("Student updated successfully.")

        elif action == "Delete Student":
            with st.form("Delete Student Form"):
                student_id = st.number_input("Student ID", min_value=1)
                submit_button = st.form_submit_button("Delete Student")
                if submit_button:
                    delete_student(student_id)
                    st.success("Student deleted successfully.")
        
        elif action == "View Faculty":
            faculty_members = view_all_faculty()
            for faculty in faculty_members:
                st.write(f"Faculty ID: {faculty[0]}, Name: {faculty[1]}, Department: {faculty[2]}")

        elif action == "Update Faculty":
            with st.form("Update Faculty Form"):
                faculty_id = st.number_input("Faculty ID", min_value=1, format="%d")
                new_name = st.text_input("New Faculty Name")
                new_department = st.text_input("New Department")
                submit_button = st.form_submit_button("Update Faculty")
                if submit_button:
                    update_faculty(faculty_id, new_name, new_department)
                    st.success("Faculty updated successfully.")




    if st.session_state.role_name == 'HOD':
        st.header("Head of Department Dashboard")
        hod_action = st.selectbox("Select Action", ["View Student", "Add Student", "Update Student", "Delete Student", 
                                            "View Faculty", "Add Faculty", "Update Faculty", "Delete Faculty"])

        if hod_action == "View Student":
            students = view_students()  # Assuming `view_students` fetches all students
            for student in students:
                st.write(f"Student ID: {student[0]}, Name: {student[1]}, Department: {student[2]}, Year: {student[3]}")

        elif hod_action == "Add Student":
            with st.form("Add Student Form"):
                name = st.text_input("Student Name")
                department = st.text_input("Department")
                year = st.number_input("Year", min_value=1)
                faculty_id = st.number_input("Faculty ID", min_value=1, format="%d")
                submit_button = st.form_submit_button("Add Student")
                if submit_button:
                    add_student(name, department, year, faculty_id)
                    st.success("Student added successfully.")

        elif hod_action == "Update Student":
            with st.form("Update Student Form"):
                student_id = st.number_input("Student ID", min_value=1)
                new_name = st.text_input("New Student Name")
                new_department = st.text_input("New Department")
                new_year = st.number_input("New Year", min_value=1)
                submit_button = st.form_submit_button("Update Student")
                if submit_button:
                    update_student(student_id, new_name, new_department, new_year)
                    st.success("Student updated successfully.")

        elif hod_action == "Delete Student":
            with st.form("Delete Student Form"):
                student_id = st.number_input("Student ID", min_value=1)
                submit_button = st.form_submit_button("Delete Student")
                if submit_button:
                    delete_student(student_id)
                    st.success("Student deleted successfully.")

        elif hod_action == "View Faculty":
            faculty_members = view_all_faculty()
            for faculty in faculty_members:
                st.write(f"Faculty ID: {faculty[0]}, Name: {faculty[1]}, Department: {faculty[2]}")

        elif hod_action == "Add Faculty":
            with st.form("Add Faculty Form"):
                name = st.text_input("Faculty Name")
                department = st.text_input("Department")
                submit_button = st.form_submit_button("Add Faculty")
                if submit_button:
                    add_faculty(name, department)
                    st.success("Faculty added successfully.")

        elif hod_action == "Update Faculty":
            with st.form("Update Faculty Form"):
                faculty_id = st.number_input("Faculty ID", min_value=1, format="%d")
                new_name = st.text_input("New Faculty Name")
                new_department = st.text_input("New Department")
                submit_button = st.form_submit_button("Update Faculty")
                if submit_button:
                    update_faculty(faculty_id, new_name, new_department)
                    st.success("Faculty updated successfully.")

        elif hod_action == "Delete Faculty":
            with st.form("Delete Faculty Form"):
                faculty_id = st.number_input("Faculty ID", min_value=1, format="%d")
                submit_button = st.form_submit_button("Delete Faculty")
                if submit_button:
                    delete_faculty(faculty_id)
                    st.success("Faculty deleted successfully.")


        
    elif st.session_state.role_name == 'Student':
        st.header("Student Dashboard")
        student_action = st.selectbox("Select Action", ["View My Details", "Update My Details"])
    
        
        if student_action == "View Your Details":
            student_id = st.number_input("Enter Student ID", min_value=1, format="%d")
            if st.button("View"):
                student = view_students(student_id)
                if student:
                    st.write(f"Student ID: {student[0]}, Name: {student[1]}, Department: {student[5]}, Year: {student[3]}")
                else:
                    st.error("No student found with that ID.")

        elif student_action == "Update Your Details":
            with st.form("Update Student Details Form"):
                student_id = st.number_input("Student ID", min_value=1, format="%d")
                new_name = st.text_input("New Name")
                new_department = st.text_input("New Department")
                new_year = st.number_input("New Year", min_value=1)
                submit_button = st.form_submit_button("Update Details")
                if submit_button:
                    update_student(student_id, new_name, new_department, new_year)
                    st.success("Your details have been updated.")
    
    elif st.session_state.role_name == 'Faculty Advisor':
        st.header("Faculty Advisor Dashboard")
        action = st.selectbox("Select Action", ["View Student Details", "Update Student Details", "View Faculty Details"])

        if action == "View Student Details":
            student_id = st.number_input("Enter Student ID to View", min_value=1, format="%d")
            if st.button("View Student"):
                student = view_students(student_id)
                if student:
                    st.write(f"Student ID: {student[0]}, Name: {student[1]}, Department: {student[5]}, Year: {student[3]}")
                else:
                    st.error("No student found with that ID.")

        elif action == "Update Student Details":
            with st.form("Update Student Details Form"):
                student_id = st.number_input("Student ID to Update", min_value=1, format="%d")
                new_name = st.text_input("New Name")
                new_department = st.text_input("New Department")
                new_year = st.number_input("New Year", min_value=1)
                submit_button = st.form_submit_button("Update Student")
                if submit_button:
                    update_student(student_id, new_name, new_department, new_year)
                    st.success("Student details have been updated.")

        elif action == "View Faculty Details":
            st.write("Faculty Details:")
            faculty_members = view_all_faculty()
            for faculty in faculty_members:
                st.write(f"Faculty ID: {faculty[0]}, Name: {faculty[1]}, Department: {faculty[2]}")


else:
    st.info("Please log in to access the system.")
