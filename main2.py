import csv
import mysql.connector

# Establish a connection to the MySQL server
connection = mysql.connector.connect(host='127.0.0.1',
                                     database='MySQL',
                                     user='root',
                                     password='Son@2003')

try:
    if connection.is_connected():
        print("Connected to MySQL Server!")

    # Create cursor
    mycursor = connection.cursor()

    # Read commands from CSV file
    filename = input("Enter the name of the CSV file: ")
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            command = row[0]
            if command == 'e':
                # Create tables if they don't exist
                TABLES = {
                    'Team': 'CREATE TABLE IF NOT EXISTS Team (Name VARCHAR(255) UNIQUE, City VARCHAR(255), State VARCHAR(25), PRIMARY KEY (Name))',
                    'Coach': 'CREATE TABLE IF NOT EXISTS Coach (SSN VARCHAR(9) UNIQUE, Name VARCHAR(255), PRIMARY KEY (SSN))',
                    'Appointment': 'CREATE TABLE IF NOT EXISTS Appointment (Team VARCHAR(255), Coach VARCHAR(9), StartDate DATE, EndDate DATE, PRIMARY KEY (Team, Coach), FOREIGN KEY (Team) REFERENCES Team(Name), FOREIGN KEY (Coach) REFERENCES Coach(SSN))',
                    'Games': 'CREATE TABLE IF NOT EXISTS Games (HomeTeam VARCHAR(255), RoadTeam VARCHAR(255), GameDate DATE, GameNumber INT, HomeScore INT, RoadScore INT, PRIMARY KEY (HomeTeam, RoadTeam, GameDate, GameNumber), FOREIGN KEY (HomeTeam) REFERENCES Team(Name), FOREIGN KEY (RoadTeam) REFERENCES Team(Name))'
                }
                for table_name, create_table_query in TABLES.items():
                    mycursor.execute(create_table_query)
                print("Tables created successfully.")
                
            elif command == 'r':
                # Clear all data from tables
                mycursor.execute("DELETE FROM Appointment")
                mycursor.execute("DELETE FROM Games")
                mycursor.execute("DELETE FROM Team")
                mycursor.execute("DELETE FROM Coach")                
                
                connection.commit();
                print("Data cleared successfully.")

            elif command == 't':
                # Add a new team
                try:
                    team_name, city, state = row[1], row[2], row[3]
                    mycursor.execute("INSERT INTO Team (Name, City, State) VALUES (%s, %s, %s)", (team_name, city, state))
                    print("New team added successfully.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'c':
                # Add a new coach
                try:
                    ssn, name = row[1], row[2]
                    mycursor.execute("INSERT INTO Coach (SSN, Name) VALUES (%s, %s)", (ssn, name))
                    print("New coach added successfully.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)
            elif command == 'h':
                try:
                        # Hire a new coach
                    team_name, coach_ssn, hire_date = row[1], row[2], row[3]

                    # Check if the coach exists in the Coach table
                    mycursor.execute("SELECT COUNT(*) FROM Coach WHERE SSN = %s", (coach_ssn,))
                    coach_count = mycursor.fetchone()[0]

                    if coach_count == 0:
                        print("Error: Coach with provided SSN does not exist.")
                    else:
                        mycursor.execute("SELECT COUNT(*) FROM Appointment WHERE Team = %s AND EndDate IS NULL", (team_name,))
                        existing_coach_count = mycursor.fetchone()[0]
                    
                        if existing_coach_count > 0:
                            print("Error: This team already has a coach. Cannot hire a new coach.")
                        else:
                            # Hire a new coach
                            mycursor.execute("INSERT INTO Appointment (Team, Coach, StartDate) VALUES (%s, %s, %s)", (team_name, coach_ssn, hire_date))
                            print("New coach hired successfully.")      
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)  
                except Exception as e:
                    print("Invalid Input ", e)      
            elif command == 'f':
                # Fire a coach
                try:
                    team_name, fire_date = row[1], row[2]
                    mycursor.execute("UPDATE Appointment SET EndDate = %s WHERE Team = %s AND EndDate IS NULL", (fire_date, team_name))
                    print("Coach fired successfully.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'g':
                    # Enter info of a game
                try:
                    game_date, home_team, road_team = row[1], row[2], row[3]

                    # Check if both HomeTeam and RoadTeam exist in the Team table
                    mycursor.execute("SELECT COUNT(*) FROM Team WHERE Name IN (%s, %s)", (home_team, road_team))
                    team_count = mycursor.fetchone()[0]

                    if team_count == 2:
                        # Set GameNumber to 1 by default
                        game_number = 1
                    
                        # Check if the same teams have played against each other on the same date before
                        mycursor.execute("SELECT MAX(GameNumber) FROM Games WHERE GameDate = %s AND ((HomeTeam = %s AND RoadTeam = %s) OR (HomeTeam = %s AND RoadTeam = %s))", (game_date, home_team, road_team, road_team, home_team))
                        max_game_number = mycursor.fetchone()[0]
                        
                        # If they have played before, increment GameNumber
                        if max_game_number:
                            game_number = max_game_number + 1

                        # Insert game info with GameNumber
                        mycursor.execute("INSERT INTO Games (GameDate, HomeTeam, RoadTeam, GameNumber) VALUES (%s, %s, %s, %s)", (game_date, home_team, road_team, game_number))
                        print("Game info added successfully.")
                    else:
                        print("Error: Invalid team names.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 's':
                try:
                    game_date, home_team, road_team, home_score, road_score = row[1], row[2], row[3], row[4], row[5]

                    # Check if the game exists in the Games table
                    mycursor.execute("SELECT COUNT(*) FROM Games WHERE GameDate = %s AND HomeTeam = %s AND RoadTeam = %s AND HomeScore IS NULL AND RoadScore IS NULL", (game_date, home_team, road_team))
                    game_count = mycursor.fetchone()[0]

                    if game_count > 0:
                        # Update the first game without a score
                        mycursor.execute("UPDATE Games SET HomeScore = %s, RoadScore = %s WHERE GameDate = %s AND HomeTeam = %s AND RoadTeam = %s AND HomeScore IS NULL AND RoadScore IS NULL LIMIT 1", (home_score, road_score, game_date, home_team, road_team))
                        print("Game score added successfully.")
                    else:
                        print("Error: No eligible game found for the provided teams and date.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'T':
                try:
                    # Return team information
                    team_name = row[1]
                    mycursor.execute("SELECT * FROM Team WHERE Name = %s", (team_name,))
                    team_data = mycursor.fetchone()
                    if team_data:
                        print(f"Team: {team_data[0]}, City: {team_data[1]}, State: {team_data[2]}")
                        mycursor.execute("SELECT Coach, StartDate, EndDate FROM Appointment WHERE Team = %s ORDER BY StartDate", (team_name,))
                        coaches = mycursor.fetchall()
                        for coach in coaches:
                            coach_ssn = coach[0]
                            mycursor.execute("SELECT Name FROM Coach WHERE SSN = %s", (coach_ssn,))
                            coach_name = mycursor.fetchone()[0]
                            print(f"Coach: {coach_name}, Start Date: {coach[1]}, End Date: {coach[2]}")
                    else:
                        print("Team not found.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'C':
                try:
                        # Return coach information
                    coach_ssn = row[1]
                    mycursor.execute("SELECT * FROM Coach WHERE SSN = %s", (coach_ssn,))
                    coach_data = mycursor.fetchone()
                    if coach_data:
                        coach_name = coach_data[1]
                        print(f"SSN: {coach_ssn}, Name: {coach_name}")
                        
                        mycursor.execute("SELECT Team, StartDate, EndDate FROM Appointment WHERE Coach = %s", (coach_ssn,))
                        teams = mycursor.fetchall()
                        for team in teams:
                            team_name = team[0]
                            print(f"Team: {team[0]} ")
                        mycursor.execute("SELECT Coach, StartDate, EndDate FROM Appointment WHERE Team = %s ORDER BY StartDate", (team_name,))
                        coaches1 = mycursor.fetchall()
                        for coach in coaches1:
                            print(f"Start Date: {coach[1]}, End Date: {coach[2]}")    
                        
                    else:
                        print("Coach not found.")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)
            elif command == 'G':
                try:
                    # Return information about games played by two teams
                    team1, team2 = row[1], row[2]
                    mycursor.execute("SELECT * FROM Games WHERE (HomeTeam = %s AND RoadTeam = %s) ", (team1, team2))
                    games = mycursor.fetchall()
                    for game in games:
                        print(f"Date: {game[2]}, Team 1: {game[0]}, Team 2: {game[1]}, Team 1 Score: {game[4]}, Team 2 Score: {game[5]}")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'S':
                try:
                    # Return the table of standings for a period
                    start_date, end_date = row[1], row[2]

                    mycursor.execute("SELECT Team, SUM(CASE WHEN HomeTeam = Team THEN HomeScore ELSE RoadScore END) AS TotalScore, SUM(CASE WHEN HomeTeam = Team THEN RoadScore ELSE HomeScore END) AS OpponentScore, COUNT(*) AS GamesPlayed FROM Games WHERE GameDate BETWEEN %s AND %s GROUP BY Team", (start_date, end_date))
                    standings_data = mycursor.fetchall()

                    standings = []
                    for team_data in standings_data:
                        team_name, total_score, opponent_score, games_played = team_data
                        mycursor.execute("SELECT COUNT(*) FROM Games WHERE GameDate BETWEEN %s AND %s AND ((HomeTeam = %s AND HomeScore > RoadScore) OR (RoadTeam = %s AND RoadScore > HomeScore))", (start_date, end_date, team_name, team_name))
                        wins = mycursor.fetchone()[0]

                        mycursor.execute("SELECT COUNT(*) FROM Games WHERE GameDate BETWEEN %s AND %s AND ((HomeTeam = %s OR RoadTeam = %s) AND HomeScore = RoadScore)", (start_date, end_date, team_name, team_name))
                        ties = mycursor.fetchone()[0]

                        losses = games_played - wins - ties
                        points = 2 * wins + ties

                        standings.append((team_name, wins, ties, losses, total_score, opponent_score, points))

                    # Sort standings based on criteria
                    standings.sort(key=lambda x: (-x[6], (x[4] - x[5]), -x[4], -x[1], x[3], x[0]))

                    # Print the standings table
                    print("Team, Wins, Ties, Losses, Total Score, Total Opponent's Score, Points")
                    for team in standings:
                        print(f"{team[0]}, {team[1]}, {team[2]}, {team[3]}, {team[4]}, {team[5]}, {team[6]}")
                except mysql.connector.Error as err:
                    print("Invalid Input ", err)
                except Exception as e:
                    print("Invalid Input ", e)

            elif command == 'H':
                # Extra query: find teams based on beating pattern
                team_a, team_b = row[1], row[2]
                mycursor.execute("SELECT DISTINCT RoadTeam FROM Games WHERE HomeTeam = %s AND GameDate BETWEEN '2000-01-01' AND '2023-11-01' UNION SELECT DISTINCT HomeTeam FROM Games WHERE RoadTeam = %s AND GameDate BETWEEN '2000-01-01' AND '2023-11-01'", (team_a, team_b))
                teams = mycursor.fetchall()
                if teams:
                    for team in teams:
                        print(f"Team: {team[0]}")
                else:
                    print("No teams found.")

            else:
                print("Invalid input")

    # Commit the changes
    connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    mycursor.close()
    connection.close()


create_department_table = """
CREATE TABLE Department(
DeptName VARCHAR(40) PRIMARY KEY,
DeptID VARCHAR(4) UNIQUE NOT NULL
)
"""

create_faculty_table = """
CREATE TABLE Faculty(
FacultyID CHAR(8) PRIMARY KEY,
Name VARCHAR(40) NOT NULL,
Email VARCHAR(40) UNIQUE NOT NULL,
DeptID VARCHAR(4) NOT NULL,
Position ENUM('Full', 'Associate', 'Assistant', 'Adjunct') NOT NULL,
FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
)
"""

create_program_table = """
CREATE TABLE Program(
ProgName VARCHAR(50) NOT NULL,
DeptID VARCHAR(4) NOT NULL,
FacultyLead VARCHAR(40) NOT NULL,
FacultyLeadID VARCHAR(8) NOT NULL,
FacultyLeadEmail VARCHAR(40) NOT NULL,
PRIMARY KEY (ProgName, DeptID),
FOREIGN KEY (DeptID) REFERENCES Department(DeptID),
FOREIGN KEY (FacultyLeadID) REFERENCES Faculty(FacultyID),
FOREIGN KEY (FacultyLeadEmail) REFERENCES Faculty(Email)
)
"""

create_course_table = """
CREATE TABLE Course(
CourseID VARCHAR(8) PRIMARY KEY,
Title VARCHAR(80) NOT NULL,
Description TEXT,
DeptID VARCHAR(4) NOT NULL,
FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
)
"""

create_section_table = """
CREATE TABLE Section(
SecID CHAR(3) NOT NULL,
CourseID VARCHAR(8) NOT NULL,
Semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
Year YEAR NOT NULL,
FacultyLeadID CHAR(8) NOT NULL,
EnrollCount SMALLINT NOT NULL,
PRIMARY KEY (CourseID, SecID, Semester, Year),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
FOREIGN KEY (FacultyLeadID) REFERENCES Faculty(FacultyID)
)
"""

create_objectives_table = """
CREATE TABLE Objectives(
ObjCode VARCHAR(10) NOT NULL,
Description TEXT NOT NULL,
ProgName VARCHAR(50) NOT NULL,
DeptID VARCHAR(4) NOT NULL,
PRIMARY KEY (ObjCode),
FOREIGN KEY (DeptID) REFERENCES Department(DeptID),
FOREIGN KEY (ProgName) REFERENCES Program(ProgName)
)
"""

create_sub_objectives_table = """
CREATE TABLE SubObjectives(
SubObjCode VARCHAR(12) PRIMARY KEY,
Description TEXT NOT NULL,
ObjCode VARCHAR(10) NOT NULL,
FOREIGN KEY (ObjCode) REFERENCES Objectives(ObjCode)
)
"""

create_course_objectives_table = """
CREATE TABLE CourseObjectives(
CourseObjID VARCHAR(24) PRIMARY KEY,
CourseID VARCHAR(8) NOT NULL,
ObjCode VARCHAR(10) NOT NULL,
SubObjCode VARCHAR(12),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
FOREIGN KEY (ObjCode) REFERENCES Objectives(ObjCode)
)
"""


create_objective_eval_table = """
CREATE TABLE ObjectiveEval(
CourseObjID VARCHAR(24) NOT NULL,
SecID CHAR(3) NOT NULL,
Semester ENUM('Fall', 'Spring', 'Summer') NOT NULL,
Year YEAR NOT NULL,
EvalMethod ENUM('Exam', 'Project', 'Assignment', 'Interview', 'Presentation') NOT NULL,
StudentsPassed SMALLINT NOT NULL,
FOREIGN KEY (CourseObjID) REFERENCES CourseObjectives(CourseObjID)
)
"""

clear_tables = [
    "TRUNCATE TABLE Program;",
    "TRUNCATE TABLE Department;",
    "TRUNCATE TABLE Faculty;",
    "TRUNCATE TABLE Course;",
    "TRUNCATE TABLE Section;",
    "TRUNCATE TABLE Objectives;",
    "TRUNCATE TABLE SubObjectives;",
    "TRUNCATE TABLE CourseObjectives;",
    "TRUNCATE TABLE ObjectiveEval;"
]

count_obj_query = """
SELECT COUNT(*) AS obj_count
    FROM Objectives
    WHERE ProgName = %s
    AND DeptID = %s
"""


count_sub_obj_query = """
SELECT COUNT(*) AS sub_obj_count
    FROM SubObjectives
    WHERE ObjCode = %s
"""


get_sub_objectives = """
SELECT SubObjCode
    FROM SubObjectives
    WHERE ObjCode = %s
"""


check_obj_exists = """
SELECT COUNT(*) AS obj_count
    FROM Objectives
    WHERE ObjCode = %s
"""


check_course_exists = """
SELECT COUNT(*) AS course_count
    FROM Course
    WHERE CourseID = %s
"""


check_sub_obj_exists = """
SELECT COUNT(*) AS sub_obj_count
    FROM SubObjectives
    WHERE SubObjCode = %s
"""

check_course_obj_id_exists = """
SELECT COUNT(*) AS course_obj_count
    FROM CourseObjectives
    WHERE CourseObjID = %s
"""


check_section_exists = """
SELECT COUNT(*) AS section_count
    FROM Section
    WHERE CourseID = %s
    AND SecID = %s
    AND Semester = %s
    AND Year = %s
"""


get_student_count = """
SELECT EnrollCount
    FROM Section
    WHERE CourseID = %s
    AND SecID = %s
    AND Semester = %s
    AND Year = %s
"""