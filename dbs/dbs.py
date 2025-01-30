import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kavitha07@",
    database="dbs"
)
cursor = db.cursor()

# Example permissions array based on your descriptions
# Indexes correspond to:
# 0: Can View Students
# 1: Can Add Students
# 2: Can Update Students
# 3: Can Delete Students
# 4: Can View Faculty
# 5: Can Update Faculty
# etc.

roles = {
    'HOD': [True, True, True, True, True, True],  # Permissions for HOD
    'Academic Advisor': [True, False, True, False, True, True],  # Updated for Academic Advisor
    'Faculty Advisor': [True, False, True, False, True, False],  # Permissions for Faculty Advisor
    'Student': [True, False, False, False, False, False]  # Permissions for Student
}

# Authenticate user and retrieve role permissions
def authenticate_user(username, password):
    cursor.execute("SELECT user_id, role_id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        user_id, role_id = user
        cursor.execute("SELECT role_name FROM roles WHERE role_id = %s", (role_id,))
        role_name = cursor.fetchone()[0]
        return user_id, role_name, roles[role_name]
    else:
        print("Authentication failed.")
        return None, None, None

# Function to view student details
def view_student(student_id, role_permissions):
    if role_permissions[0]:  # Can view students
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        if student:
            # Fetch faculty name based on faculty_id
            cursor.execute("SELECT name FROM faculty WHERE faculty_id = %s", (student[4],))
            faculty = cursor.fetchone()
            faculty_name = faculty[0] if faculty else "Unknown"
            print("Student Details: (ID: {}, Name: {}, Department: {}, Year: {}, Faculty: {})".format(student[0], student[1], student[2], student[3], faculty_name))
        else:
            print("No student found with that ID.")
    else:
        print("Access denied: You do not have permission to view student records.")

# Function to add a student
def add_student(name, department, year, faculty_id, role_permissions):
    if role_permissions[1]:  # Can add students
        sql = "INSERT INTO students (name, department, year, faculty_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, department, year, faculty_id))
        db.commit()
        print("Student added successfully.")
    else:
        print("Access denied: You do not have permission to add students.")

# Function to update student details
def update_student(student_id, new_name, new_department, new_year, role_permissions):
    if role_permissions[2]:  # Can update students
        sql = "UPDATE students SET name = %s, department = %s, year = %s WHERE student_id = %s"
        cursor.execute(sql, (new_name, new_department, new_year, student_id))
        db.commit()
        print("Student record updated successfully.")
    else:
        print("Access denied: You do not have permission to update students.")

# Function to delete a student
def delete_student(student_id, role_permissions):
    if role_permissions[3]:  # Can delete students
        sql = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        db.commit()
        print("Student record deleted successfully.")
    else:
        print("Access denied: You do not have permission to delete students.")

# Function to view faculty member's details
def view_faculty(faculty_id, role_permissions):
    if role_permissions[4]:  # Can view faculty
        cursor.execute("SELECT * FROM faculty WHERE faculty_id = %s", (faculty_id,))
        faculty = cursor.fetchone()
        if faculty:
            print("Faculty Details: (ID: {}, Name: {}, Department: {})".format(faculty[0], faculty[1], faculty[2]))
        else:
            print("No faculty found with that ID.")
    else:
        print("Access denied: You do not have permission to view faculty records.")

# Function to update faculty member's details
def update_faculty(faculty_id, new_name, new_department, role_permissions):
    if role_permissions[5]:  # Can update faculty
        sql = "UPDATE faculty SET name = %s, department = %s WHERE faculty_id = %s"
        cursor.execute(sql, (new_name, new_department, faculty_id))
        db.commit()
        print("Faculty record updated successfully.")
    else:
        print("Access denied: You do not have permission to update faculty records.")

# Main function
def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    user_id, role_name, role_permissions = authenticate_user(username, password)
    
    if role_permissions is not None:
        while True:
            print("\n1. View Student\n2. Add Student\n3. Update Student\n4. Delete Student\n5. View Faculty\n6. Update Faculty\n7. Exit")
            choice = int(input("Choose an option: "))
            
            if choice == 1:
                student_id = int(input("Enter student ID: "))
                view_student(student_id, role_permissions)
            elif choice == 2:
                name = input("Enter student name: ")
                department = input("Enter student department: ")
                year = int(input("Enter student year: "))
                faculty_id = int(input("Enter faculty ID: "))
                add_student(name, department, year, faculty_id, role_permissions)
            elif choice == 3:
                student_id = int(input("Enter student ID: "))
                new_name = input("Enter new student name: ")
                new_department = input("Enter new department: ")
                new_year = int(input("Enter new year: "))
                update_student(student_id, new_name, new_department, new_year, role_permissions)
            elif choice == 4:
                student_id = int(input("Enter student ID: "))
                delete_student(student_id, role_permissions)
            elif choice == 5:
                faculty_id = int(input("Enter faculty ID: "))
                view_faculty(faculty_id, role_permissions)
            elif choice == 6:
                faculty_id = int(input("Enter faculty ID: "))
                new_name = input("Enter new faculty name: ")
                new_department = input("Enter new department: ")
                update_faculty(faculty_id, new_name, new_department, role_permissions)
            elif choice == 7:
                print("Exiting...")
                break
            else:
                print("Invalid option, please try again.")
    else:
        print("Login failed or access denied.")

# Run the main function
if __name__ == "__main__":
    main()
