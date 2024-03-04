import mysql.connector
from tkinter import Tk, Label, Entry, Button, StringVar, Listbox, messagebox, Frame
# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    database = 'databaseproject',
    user='root',
    password='Son@2003'
)
cursor = conn.cursor()
# Create the Tkinter app1lication
app1 = Tk()
app1.title("User Data Entry")
app2 = Tk()
app2.title("User Query Input")
# Function to add basic information about Departments
def add_department():
    department_name = department_name_entry.get()
    department_code = department_code_entry.get()

    # Insert data into the Departments table
    try:
        cursor.execute("INSERT INTO Departments (DepartmentName, DepartmentCode) VALUES (%s, %s)",
                       (department_name, department_code))
        conn.commit()
        messagebox.showinfo("Success", "Department added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding department: {str(e)}")

# Function to add basic information about Faculty
def add_faculty():
    faculty_id = faculty_id_entry.get()
    faculty_name = faculty_name_entry.get()
    faculty_email = faculty_email_entry.get()
    faculty_rank = faculty_rank_entry.get()
    department_code = department_code_faculty_entry.get()

    # Insert data into the Faculty table
    try:
        cursor.execute("INSERT INTO Faculty (FacultyName, FacultyEmail, FacultyRank, DepartmentCode, FacultyID) VALUES (%s, %s, %s, %s, %s)",
                       (faculty_name, faculty_email, faculty_rank, department_code, faculty_id))
        conn.commit()
        messagebox.showinfo("Success", "Faculty member added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding faculty: {str(e)}")

# Function to add basic information about Programs
def add_program():
    program_name = program_name_entry.get()
    faculty_id = faculty_id_program_entry.get()
    department_code = department_code_program_entry.get()

    # Insert data into the Programs table
    try:
        cursor.execute("INSERT INTO Programs (ProgramName, FacultyID, DepartmentCode) VALUES (%s, %s, %s)",
                       (program_name, faculty_id, department_code))
        conn.commit()
        messagebox.showinfo("Success", "Program added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding program: {str(e)}")

# Function to add basic information about Courses
def add_course():
    course_id = course_id_entry.get()
    title = course_title_entry.get()
    description = course_description_entry.get()
    department_code = department_code_course_entry.get()
    program_name = program_name_course_entry.get()

    # Insert data into the Courses table
    try:
        cursor.execute("INSERT INTO Courses (CourseID, Title, Description, DepartmentCode, ProgramName) VALUES (%s, %s, %s, %s, %s)",
                       (course_id, title, description, department_code, program_name))
        conn.commit()
        messagebox.showinfo("Success", "Course added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding course: {str(e)}")

# Function to add basic information about Sections
def add_section():
    course_id = course_id_entry_section.get()
    semester = semester_entry.get()
    section_number = section_number_entry.get()
    year = year_entry.get()
    enroll_num = enroll_num_entry.get()
    faculty_id = faculty_id_entry_section.get()

    # Insert data into the Sections table
    try:
        cursor.execute("INSERT INTO Sections (CourseID, Semester, SectionNumber, Year, EnrollNum, FacultyID) VALUES (%s, %s, %s, %s, %s, %s)",
                       (course_id, semester, section_number, year, enroll_num, faculty_id))
        conn.commit()
        messagebox.showinfo("Success", "Section added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding section: {str(e)}")

# Function to add basic information about Learning Objectives
def add_learning_objective():
    objective_code = objective_code_entry.get()
    description = objective_description_entry.get()
    program_name = program_name_learning_objective_entry.get()
    course_id = course_id_learning_objective_entry.get()

    # Insert data into the LearningObjectives table
    try:
        cursor.execute("INSERT INTO LearningObjectives (ObjectiveCode, Description, ProgramName, CourseID) VALUES (%s, %s, %s, %s)",
                       (objective_code, description, program_name, course_id))
        conn.commit()
        messagebox.showinfo("Success", "Learning objective added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding learning objective: {str(e)}")

# Function to add basic information about Sub-Objectives
def add_sub_objective():
    sub_objective_code = sub_objective_code_entry.get()
    objective_code = objective_code_sub_objective_entry.get()
    description = sub_objective_description_entry.get()
    course_id = course_id_sub_objective_entry.get()

    # Insert data into the SubObjectives table
    try:
        cursor.execute("INSERT INTO SubObjectives (SubObjectiveCode, ObjectiveCode, Description, CourseID) VALUES (%s, %s, %s, %s)",
                       (sub_objective_code, objective_code, description, course_id))
        conn.commit()
        messagebox.showinfo("Success", "Sub-objective added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding sub-objective: {str(e)}")

# Function to add basic information about Evaluation
def add_evaluation():
    course_id = evaluation_course_id_entry.get()
    sub_objective_code = evaluation_sub_objective_code_entry.get() or None
    objective_code = evaluation_objective_code_entry.get()
    eval_method = evaluation_method_entry.get()
    students_passed = students_passed_entry.get()
    semester = evaluation_semester_entry.get()
    year = evaluation_year_entry.get()
    section_number = evaluation_section_number_entry.get()

    # Insert data into the Evaluation table
    try:
        cursor.execute("INSERT INTO Evaluation (CourseID, ObjectiveCode, SubObjectiveCode, EvaluationMethod, StudentsMetObjective, Semester, Year, SectionNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (course_id, objective_code, sub_objective_code, eval_method, students_passed, semester, year, section_number))
        conn.commit()
        messagebox.showinfo("Success", "Evaluation added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding Evaluation: {str(e)}")


        

from tkinter import messagebox

# Function to list all programs for a given department
def list_programs_by_department():
    department_code = department_name_list_programs_entry.get()
    try:
        cursor.execute("SELECT ProgramName FROM Programs WHERE DepartmentCode = %s", (department_code,))
        programs = cursor.fetchall()
        
        if not programs:
            messagebox.showinfo("Programs", "No programs found for the specified department.")
        else:
            programs_text = "\n".join(program[0] for program in programs)
            messagebox.showinfo("Programs", f"Programs for the department:\n{programs_text}\n")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error listing programs: {str(e)}")

# Function to list all faculty and their program assignments for a given department
def list_faculty_by_department():
    department_code = department_name_list_faculty_entry.get()
    try:
        cursor.execute("""
            SELECT
                Faculty.FacultyID,
                Faculty.FacultyName,
                Faculty.FacultyEmail,
                Faculty.FacultyRank,
                Programs.ProgramName AS InChargeOfProgram
            FROM
                Faculty
            LEFT JOIN Programs ON Faculty.DepartmentCode = Programs.DepartmentCode
            WHERE
                Faculty.DepartmentCode = %s
        """, (department_code,))
        faculty_programs = cursor.fetchall()
        
        if not faculty_programs:
            messagebox.showinfo("Faculty", "No faculty found for the specified department.")
        else:
            faculty_text = "\n".join(f"{faculty_program[1]} - {faculty_program[4]}" for faculty_program in faculty_programs)
            messagebox.showinfo("Faculty", f"Faculty for the department:\n{faculty_text}\n")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error listing faculty: {str(e)}")


# Function to list all courses and objectives/sub-objectives association for a given program and year
def list_courses_objectives_by_program():
    program_name = program_name_list_courses_entry.get()
    try:
        cursor.execute("""
            SELECT
                Courses.CourseID,
                Courses.Title,
                Courses.Description,
                LearningObjectives.ObjectiveCode,
                LearningObjectives.Description AS ObjectiveDescription,
                SubObjectives.SubObjectiveCode,
                SubObjectives.Description AS SubObjectiveDescription,
                Sections.Year
            FROM
                Courses
            LEFT JOIN LearningObjectives ON Courses.CourseID = LearningObjectives.CourseID
            LEFT JOIN SubObjectives ON LearningObjectives.ObjectiveCode = SubObjectives.ObjectiveCode
            LEFT JOIN Sections ON Courses.CourseID = Sections.CourseID
            WHERE
                Courses.ProgramName = %s 
        """, (program_name,))
        
        courses_objectives = cursor.fetchall()
        
        if not courses_objectives:
            messagebox.showinfo("Courses and Objectives", "No courses and objectives found for the specified program.")
        else:
            courses_text = "\n".join(f"Course ID: {course_objective[0]}, Title: {course_objective[1]}, "
                                     f"Description: {course_objective[2]}, Objective Code: {course_objective[3]}, "
                                     f"Objective Description: {course_objective[4]}, "
                                     f"Sub-Objective Code: {course_objective[5]}, "
                                     f"Sub-Objective Description: {course_objective[6]}, "
                                     f"Year: {course_objective[7]}\n" for course_objective in courses_objectives)
            messagebox.showinfo("Courses and Objectives", f"Courses and Objectives for the program:\n{courses_text}\n")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error listing courses and objectives: {str(e)}")

# Function to list all objectives for a given program
def list_objectives_by_program():
    program_name = program_name_list_objectives_entry.get()
    try:
        cursor.execute("""
            SELECT
                LearningObjectives.ObjectiveCode,
                LearningObjectives.Description AS ObjectiveDescription
            FROM
                LearningObjectives
            WHERE
                LearningObjectives.ProgramName = %s
        """, (program_name,))
        
        objectives = cursor.fetchall()
        
        if not objectives:
            messagebox.showinfo("Objectives", "No objectives found for the specified program.")
        else:
            objectives_text = "\n".join(f"Objective Code: {objective[0]}, Objective Description: {objective[1]}\n" for objective in objectives)
            messagebox.showinfo("Objectives", f"Objectives for the program:\n{objectives_text}\n")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error listing objectives: {str(e)}")


## Function to list evaluation results for each section in a given semester and program
def list_evaluation_results_by_semester_program():
    semester = semester_eval_results_entry.get()
    program_name = program_name_eval_results_entry.get()
    try:
        query = """
        SELECT
            Sections.CourseID,
            Sections.SectionNumber,
            Evaluation.EvaluationMethod,
            Evaluation.StudentsMetObjective
        FROM
            Sections
        LEFT JOIN Evaluation ON Sections.CourseID = Evaluation.CourseID
        WHERE
            Sections.Semester = %s
            AND Sections.CourseID IN (SELECT CourseID FROM Courses WHERE ProgramName = %s);
        """
        cursor.execute(query, (semester, program_name))
        evaluation_results = cursor.fetchall()

        if not evaluation_results:
            messagebox.showinfo("Evaluation Results", "No evaluation results found for the specified semester and program.")
        else:
            results_text = "\n".join(f"Section: {result[1]}, Method: {result[2] if result[2] is not None else 'Not Found'}, "
                                     f"Students Met Objective: {result[3] if result[3] is not None else 'Not Found'}\n" for result in evaluation_results)
            messagebox.showinfo("Evaluation Results", f"Evaluation Results for the semester and program:\n{results_text}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Error listing evaluation results: {str(e)}")


# Function to list evaluation results for each objective/sub-objective in a given academic year
def list_evaluation_results_by_academic_year():
    start_year = start_year_eval_results_entry.get()
    end_year = end_year_eval_results_entry.get()
    try:
        cursor.execute("""
            SELECT
                E.ObjectiveCode,
                LO.Description AS ObjectiveDescription,
                E.SubObjectiveCode,
                SO.Description AS SubObjectiveDescription,
                E.CourseID,
                S.SectionNumber,
                E.EvaluationMethod,
                SUM(E.StudentsMetObjective) AS StudentsMetObjective,
                (SUM(E.StudentsMetObjective) / S.EnrollNum * 100) AS PercentageStudentsMetObjective
            FROM
                Evaluation E
            LEFT JOIN LearningObjectives LO ON E.ObjectiveCode = LO.ObjectiveCode
            LEFT JOIN SubObjectives SO ON E.SubObjectiveCode = SO.SubObjectiveCode
            LEFT JOIN Sections S ON E.CourseID = S.CourseID AND E.Semester = S.Semester AND E.Year = S.Year AND E.SectionNumber = S.SectionNumber
            WHERE
                E.Year BETWEEN %s AND %s
            GROUP BY
                E.ObjectiveCode, LO.Description, E.SubObjectiveCode, SO.Description, E.CourseID, S.SectionNumber, E.EvaluationMethod, S.EnrollNum
        """, (start_year, end_year))
        evaluation_results = cursor.fetchall()

        if not evaluation_results:
            messagebox.showinfo("Evaluation Results", "No evaluation results found for the specified academic year.")
        else:
            results_text = "\n".join(f"Objective: {result[0]}, Objective Description: {result[1]}, "
                                     f"Sub-Objective: {result[2]}, Sub-Objective Description: {result[3]}, "
                                     f"CourseID: {result[4]}, Section: {result[5]}, "
                                     f"Method: {result[6] if result[6] is not None else 'Not Found'}, "
                                     f"Students Met Objective: {result[7] if result[7] is not None else 'Not Found'}, "
                                     f"Percentage Students Met Objective: {result[8] if result[8] is not None else 'Not Found'}%\n" for result in evaluation_results)
            messagebox.showinfo("Evaluation Results", f"Evaluation Results for the academic year:\n{results_text}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Error listing evaluation results: {str(e)}")




# GUI components for Departments
Label(app1, text="Department Name:").grid(row=0, column=0)
department_name_entry = Entry(app1)
department_name_entry.grid(row=0, column=1)

Label(app1, text="Department Code:").grid(row=0, column=2)
department_code_entry = Entry(app1)
department_code_entry.grid(row=0, column=3)

Button(app1, text="Add Department", command=add_department).grid(row=0, column=4)

# Blank rows
Label(app1, text="").grid(row=1, column=0)
Label(app1, text="").grid(row=2, column=0)

# GUI components for Faculty
Label(app1, text="Faculty Name:").grid(row=0, column=5)
faculty_name_entry = Entry(app1)
faculty_name_entry.grid(row=0, column=6)

Label(app1, text="Faculty Email:").grid(row=0, column=7)
faculty_email_entry = Entry(app1)
faculty_email_entry.grid(row=0, column=8)

Label(app1, text="Faculty Rank:").grid(row=0, column=9)
faculty_rank_entry = Entry(app1)
faculty_rank_entry.grid(row=0, column=10)

Label(app1, text="Department Code:").grid(row=1, column=5)
department_code_faculty_entry = Entry(app1)
department_code_faculty_entry.grid(row=1, column=6)

Label(app1, text="Faculty ID:").grid(row=1, column=7)
faculty_id_entry = Entry(app1)
faculty_id_entry.grid(row=1, column=8)

Button(app1, text="Add Faculty", command=add_faculty).grid(row=1, column=9)

# Blank rows
Label(app1, text="").grid(row=3, column=0)
Label(app1, text="").grid(row=4, column=0)
# GUI components for Programs
Label(app1, text="Program Name:").grid(row=5, column=0)
program_name_entry = Entry(app1)
program_name_entry.grid(row=5, column=1)

Label(app1, text="Faculty ID:").grid(row=5, column=2)
faculty_id_program_entry = Entry(app1)
faculty_id_program_entry.grid(row=5, column=3)

Label(app1, text="Department Code:").grid(row=5, column=4)
department_code_program_entry = Entry(app1)
department_code_program_entry.grid(row=5, column=5)

Button(app1, text="Add Program", command=add_program).grid(row=5, column=6)


# Blank rows
Label(app1, text="").grid(row=7, column=0)
Label(app1, text="").grid(row=8, column=0)

# GUI components for Courses
Label(app1, text="Course ID:").grid(row=9, column=0)
course_id_entry = Entry(app1)
course_id_entry.grid(row=9, column=1)

Label(app1, text="Title:").grid(row=9, column=2)
course_title_entry = Entry(app1)
course_title_entry.grid(row=9, column=3)

Label(app1, text="Description:").grid(row=9, column=4)
course_description_entry = Entry(app1)
course_description_entry.grid(row=9, column=5)

Label(app1, text="Department Code:").grid(row=10, column=0)
department_code_course_entry = Entry(app1)
department_code_course_entry.grid(row=10, column=1)

Label(app1, text="Program Name:").grid(row=10, column=2)
program_name_course_entry = Entry(app1)
program_name_course_entry.grid(row=10, column=3)

Button(app1, text="Add Course", command=add_course).grid(row=10, column=4)

# Blank rows
Label(app1, text="").grid(row=11, column=0)
Label(app1, text="").grid(row=12, column=0)

# GUI components for Sections
Label(app1, text="Course ID:").grid(row=13, column=0)
course_id_entry_section = Entry(app1)
course_id_entry_section.grid(row=13, column=1)

Label(app1, text="Semester:").grid(row=13, column=2)
semester_entry = Entry(app1)
semester_entry.grid(row=13, column=3)

Label(app1, text="Section Number:").grid(row=13, column=4)
section_number_entry = Entry(app1)
section_number_entry.grid(row=13, column=5)

Label(app1, text="Year:").grid(row=14, column=0)
year_entry = Entry(app1)
year_entry.grid(row=14, column=1)

Label(app1, text="Enroll Number:").grid(row=14, column=2)
enroll_num_entry = Entry(app1)
enroll_num_entry.grid(row=14, column=3)

Label(app1, text="Faculty ID:").grid(row=14, column=4)
faculty_id_entry_section = Entry(app1)
faculty_id_entry_section.grid(row=14, column=5)

Button(app1, text="Add Section", command=add_section).grid(row=14, column=6)

# Blank rows
Label(app1, text="").grid(row=15, column=0)
Label(app1, text="").grid(row=16, column=0)

# GUI components for Learning Objectives
Label(app1, text="Objective Code:").grid(row=17, column=0)
objective_code_entry = Entry(app1)
objective_code_entry.grid(row=17, column=1)

Label(app1, text="Description:").grid(row=17, column=2)
objective_description_entry = Entry(app1)
objective_description_entry.grid(row=17, column=3)

Label(app1, text="Program Name:").grid(row=17, column=4)
program_name_learning_objective_entry = Entry(app1)
program_name_learning_objective_entry.grid(row=17, column=5)

Label(app1, text="Course ID:").grid(row=18, column=0)
course_id_learning_objective_entry = Entry(app1)
course_id_learning_objective_entry.grid(row=18, column=1)

Button(app1, text="Add Learning Objective", command=add_learning_objective).grid(row=18, column=2)

# Blank rows
Label(app1, text="").grid(row=19, column=0)
Label(app1, text="").grid(row=20, column=0)

# GUI components for Sub-Objectives
Label(app1, text="Sub-Objective Code:").grid(row=21, column=0)
sub_objective_code_entry = Entry(app1)
sub_objective_code_entry.grid(row=21, column=1)

Label(app1, text="Objective Code:").grid(row=21, column=2)
objective_code_sub_objective_entry = Entry(app1)
objective_code_sub_objective_entry.grid(row=21, column=3)

Label(app1, text="Description:").grid(row=21, column=4)
sub_objective_description_entry = Entry(app1)
sub_objective_description_entry.grid(row=21, column=5)

Label(app1, text="Course ID:").grid(row=22, column=0)
course_id_sub_objective_entry = Entry(app1)
course_id_sub_objective_entry.grid(row=22, column=1)

Button(app1, text="Add Sub-Objective", command=add_sub_objective).grid(row=22, column=2)

# Blank rows
Label(app1, text="").grid(row=23, column=0)
Label(app1, text="").grid(row=24, column=0)

# GUI components for Evaluation
Label(app1, text="Course ID:").grid(row=29, column=0)
evaluation_course_id_entry = Entry(app1)
evaluation_course_id_entry.grid(row=29, column=1)

Label(app1, text="Objective Code:").grid(row=29, column=2)
evaluation_objective_code_entry = Entry(app1)
evaluation_objective_code_entry.grid(row=29, column=3)

Label(app1, text="Sub-Objective Code:").grid(row=29, column=4)
evaluation_sub_objective_code_entry = Entry(app1)
evaluation_sub_objective_code_entry.grid(row=29, column=5)

Label(app1, text="Evaluation Method:").grid(row=30, column=0)
evaluation_method_entry = Entry(app1)
evaluation_method_entry.grid(row=30, column=1)

Label(app1, text="Students Passed:").grid(row=30, column=2)
students_passed_entry = Entry(app1)
students_passed_entry.grid(row=30, column=3)

Label(app1, text="Semester:").grid(row=30, column=4)
evaluation_semester_entry = Entry(app1)
evaluation_semester_entry.grid(row=30, column=5)

Label(app1, text="Year:").grid(row=30, column=6)
evaluation_year_entry = Entry(app1)
evaluation_year_entry.grid(row=30, column=7)

Label(app1, text="Section Number:").grid(row=30, column=8)
evaluation_section_number_entry = Entry(app1)
evaluation_section_number_entry.grid(row=30, column=9)

Button(app1, text="Add Evaluation", command=add_evaluation).grid(row=30, column=10)

# Blank rows
Label(app1, text="").grid(row=31, column=0)
Label(app1, text="").grid(row=32, column=0)

# GUI components for Querying
# List Programs by Department
Label(app2, text="Department Code (Programs):").grid(row=0, column=0)
department_name_list_programs_entry = Entry(app2)
department_name_list_programs_entry.grid(row=0, column=1)
Button(app2, text="List Programs", command=list_programs_by_department).grid(row=0, column=2, columnspan=2)

# List Faculty by Department
Label(app2, text="Department Code (Faculty):").grid(row=1, column=0)
department_name_list_faculty_entry = Entry(app2)
department_name_list_faculty_entry.grid(row=1, column=1)
Button(app2, text="List Faculty", command=list_faculty_by_department).grid(row=1, column=2, columnspan=2)

# List Courses and Objectives by Program and Year
Label(app2, text="Program Name (Courses):").grid(row=2, column=0)
program_name_list_courses_entry = Entry(app2)
program_name_list_courses_entry.grid(row=2, column=1)


Button(app2, text="List Courses/Objectives", command=list_courses_objectives_by_program).grid(row=2, column=2, columnspan=2)

# List Objectives by Program
Label(app2, text="Program Name (Objectives):").grid(row=3, column=0)
program_name_list_objectives_entry = Entry(app2)
program_name_list_objectives_entry.grid(row=3, column=1)
Button(app2, text="List Objectives", command=list_objectives_by_program).grid(row=3, column=2, columnspan=2)

# List Evaluation Results by Semester and Program
Label(app2, text="Semester (Evaluation):").grid(row=4, column=0)
semester_eval_results_entry = Entry(app2)
semester_eval_results_entry.grid(row=4, column=1)

Label(app2, text="Program Name (Evaluation):").grid(row=4, column=2)
program_name_eval_results_entry = Entry(app2)
program_name_eval_results_entry.grid(row=4, column=3)

Button(app2, text="List Evaluation Results", command=list_evaluation_results_by_semester_program).grid(row=4, column=4, columnspan=2)

# List Evaluation Results by Academic Year
Label(app2, text="Start Year (Evaluation):").grid(row=5, column=0)
start_year_eval_results_entry = Entry(app2)
start_year_eval_results_entry.grid(row=5, column=1)

Label(app2, text="End Year (Evaluation):").grid(row=5, column=2)
end_year_eval_results_entry = Entry(app2)
end_year_eval_results_entry.grid(row=5, column=3)

Button(app2, text="List Evaluation Results For Academic Year", command=list_evaluation_results_by_academic_year).grid(row=5, column=5, columnspan=2)
# Display listbox



# Start the Tkinter main loop
app2.mainloop()
app1.mainloop()
# Close the cursor and connection when the app1lication is closed
    
cursor.close()
conn.close()